from drf_app_generators.helpers import pluralize


FACTORY_IGNORE_FIELDS = ['id', 'created', 'modified', 'archived']
FACTORY_INTEGER_FIELDS = [
    'BigIntegerField',
    'IntegerField',
    'PositiveIntegerField',
    'PositiveSmallIntegerField',
    'SmallIntegerField',
]
FACTORY_FLOAT_FIELDS = [
    'FloatField',
    'MoneyField',
]
FACTORY_TEXT_FIELDS = [
    'TextField'
]

class FieldMeta(object):
    """
    This class holds meta data of a field on model.
    """

    # From django.field
    name = None
    attname = None # This will be different if it is foreign key.
    primary_key = False
    blank = False
    null = False
    unique = False
    choices = None
    default = None
    is_relation = False
    many_to_many = False
    many_to_one = False
    one_to_many = False
    one_to_one = False
    max_length = None

    # custom fields
    field_type = None # Get from class of django.field
    field_type_string = None

    # from validators
    min_value = None
    max_value = None

    # for Decimal fields
    decimal_places: [int] = 0
    max_digits: [int] = 20

    # related model
    related_model: [object] = None
    related_model_meta: [object] = None
    self_related: bool = False

    # Factory meta if has.
    factory = None

    def __init__(self, django_field=None):
        self.django_field = django_field
        self.related_model = None
        self.related_model_meta = None

    def get_meta(self):
        self.field_type = type(self.django_field)
        self.field_type_string = self.django_field.get_internal_type()
        self.name = self.django_field.name
        self.attname = self.django_field.attname
        self.primary_key = self.django_field.primary_key
        self.blank = self.django_field.blank
        self.null = self.django_field.null
        self.unique = self.django_field.unique
        self.choices = self.django_field.choices
        self.default = self.django_field.default
        self.is_relation = self.django_field.is_relation
        self.many_to_many = self.django_field.many_to_many
        self.many_to_one = self.django_field.many_to_one
        self.one_to_many = self.django_field.one_to_many
        self.one_to_one = self.django_field.one_to_one
        self.max_length = self.django_field.max_length

        if self.field_type_string == 'DecimalField':
            # get decimal attributes
            self.decimal_places = self.django_field.decimal_places
            self.max_digits = self.django_field.max_digits

        if self.field_type_string == 'ForeignKey':
            self.related_model = self.django_field.remote_field.model

        # get validators
        for validator in self.django_field.validators:
            if hasattr(validator, 'code') and validator.code == 'min_value':
                self.min_value = validator.limit_value
            elif hasattr(validator, 'code') and validator.code == 'max_value':
                self.max_value = validator.limit_value


class ModelMeta(object):
    """
    This class holds meta data of a model, attributes,
    and fields.
    """
    model: object = None # This is Django model.
    name: str = None # For example: book
    verbose_name_plural: str = None # For example: books
    object_name: str = None # the class name of model. Example: Book
    app_label: str = None # For example: books
    fields: [object] = []
    django_fields: [object] = []
    abstract: bool = False

    # Require libs for factory
    factory_required_libs: [str] = []
    factory_required_modules: [str] = []

    def __init__(self, model=None):
        self.model = model
        self.fields = []
        self.django_fields = []
        self.factory_required_libs = []
        self.factory_required_modules = []

        if self.model:
            self.get_meta()

    def build_from_name(self, name=None):
        """
        Build meta from a model name only.
        This will be called when users generate app from command line.
        """
        self.name = name.lower()
        self.verbose_name_plural = pluralize(self.name)
        self.object_name = name
        self.app_label = pluralize(self.name)

        print(self.object_name, name)

        return self

    def get_meta(self):
        """
        Build meta data for model using Django model.
        """
        _meta = self.model._meta
        self.name = _meta.model_name
        self.verbose_name_plural = _meta.verbose_name_plural
        self.object_name = _meta.object_name
        self.app_label = _meta.app_label
        self.abstract = _meta.abstract
        self.django_fields = _meta.fields

        # Adding fields
        for django_field in self.django_fields:
            field = FieldMeta(django_field=django_field)
            field.get_meta()

            # check if field has a related model.
            if field.related_model is not None:
                if field.related_model._meta.model_name == self.name:
                    # This is the case that a field has foreign key to itself
                    field.related_model_meta = self
                    field.self_related = True
                else:
                    field.related_model_meta = ModelMeta(model=field.related_model)

            # Add factory code
            factory = FactoryMeta(field=field, model=self)
            factory.generate_code()
            field.factory = factory

            # add required modules and libs
            self.factory_required_libs += factory.import_libs
            self.factory_required_modules += factory.required_factories

            self.fields.append(field)

        # make the lists unique
        self.factory_required_libs = list(
            dict.fromkeys(self.factory_required_libs))
        self.factory_required_modules = list(
            dict.fromkeys(self.factory_required_modules))

        return self


class FactoryMeta(object):
    """
    Meta data to generate factory for a field.

    Supported field type: Text, CharField, Integer, Float, Boolean.
    """
    code_line: str = None
    import_libs: [str] = []
    required_models: [str] = []

    def __init__(self, field=None, model=None):
        self.field = field
        self.model = model
        self.code_line = None
        self.import_libs = []
        self.required_factories = []

    def generate_code(self):
        field_name = self.field.name
        field_type =self.field.field_type_string

        if field_name in FACTORY_IGNORE_FIELDS:
            # skip these fields
            return

        if field_type == 'CharField':
            self.generate_char_field_code()
        elif field_type in FACTORY_INTEGER_FIELDS:
            self.generate_integer_field_code()
        elif field_type in FACTORY_FLOAT_FIELDS:
            self.generate_float_field_code()
        elif field_type == 'BooleanField':
            self.generate_boolean_field_code()
        elif field_type in FACTORY_TEXT_FIELDS:
            self.generate_text_field_code()
        elif field_type == 'DecimalField':
            self.generate_decimal_field_code()
        elif field_type == 'DateField':
            self.add_import_lib(lib='datetime')
            self.generate_date_field_code()
        elif field_type == 'DateTimeField':
            self.add_import_lib(lib='datetime')
            self.add_import_lib(lib='pytz')
            self.generate_date_time_field_code()
        elif field_type == 'ForeignKey':
            self.generate_foreign_key_code()

    def generate_char_field_code(self):
        # using sequence as default
        self.code_line = '{} = factories.Sequence(lambda n: \'{} {} %03d\' % n)' \
            .format(self.field.name, self.model.object_name, self.field.name)

    def generate_integer_field_code(self):
        min_value = self.field.min_value if self.field.min_value is not None else 0
        max_value = self.field.max_value if self.field.max_value is not None else 1000

        self.code_line = '{} = factories.FuzzyInteger({}, {})' \
            .format(self.field.name, min_value, max_value)

    def generate_float_field_code(self):
        min_value = self.field.min_value if self.field.min_value is not None else 0.00
        max_value = self.field.max_value if self.field.max_value is not None else 1000.00

        self.code_line = '{} = factories.FuzzyFloat({}, {})' \
            .format(self.field.name, min_value, max_value)

    def generate_boolean_field_code(self):
        self.code_line = '{} = factories.Faker(\'pybool\')' \
            .format(self.field.name)

    def generate_text_field_code(self):
        self.code_line = '{} = factories.Faker(\'sentence\', nb_words=10)' \
            .format(self.field.name)

    def generate_decimal_field_code(self):
        min_value = self.field.min_value if self.field.min_value is not None else 0.00
        max_value = self.field.max_value if self.field.max_value is not None else 1000.00
        self.code_line = '{} = factories.FuzzyDecimal({}, {}, {})' \
            .format(self.field.name, min_value, max_value, self.field.decimal_places)

    def generate_date_field_code(self):
        self.code_line = '{} = factories.FuzzyDate(datetime.date(2020, 1, 1))' \
            .format(self.field.name)

    def generate_date_time_field_code(self):
        self.code_line = '''{} = factories.FuzzyDateTime(
        datetime.datetime(2020, 1, 1, tzinfo=pytz.timezone(\'UTC\'))
    )'''.format(self.field.name)

    def generate_foreign_key_code(self):
        if not self.field.self_related:
            # add require factory
            self.add_required_factory(
                app_name=self.field.related_model_meta.app_label,
                model_name=self.field.related_model_meta.object_name,
            )

            self.code_line = '{} = factories.SubFactory({})' \
                .format(
                    self.field.name,
                    f'{self.field.related_model_meta.object_name}Factory'
                )
            return

        self.code_line = '{} = None'.format(self.field.name)

    def add_import_lib(self, lib):
        import_line = None

        if lib == 'datetime':
            import_line = 'import datetime'
        elif lib == 'pytz':
            import_line = 'import pytz'

        if import_line is not None and import_line not in self.import_libs:
            self.import_libs.append(import_line)

    def add_required_factory(self, app_name, model_name):
        import_line = 'from {}.factories import {}Factory' \
            .format(app_name, model_name)

        if import_line not in self.required_factories:
            self.required_factories.append(import_line)


class AppOptions(object):

    models: [str] = [] # a list of model names
    api_doc: bool = False
    nested: bool = False
    force: bool = False

    def __init__(self, models=[], api_doc=False, nested=False, force=False):
        self.models = models
        self.api_doc = api_doc
        self.nested = nested
        self.force = force


class AppConfig(object):
    """
    This contains all configuration to generate/update a Django app.
    """
    name: str = None
    name_capitalized: str = None
    options: AppOptions = AppOptions()
    models_meta: [ModelMeta] = []
    force: bool = False # force to override.

    def __init__(self, name=None, options=None, init=True):
        self.name = name
        self.name_capitalized = self.name.capitalize()
        self.options = options
        self.init = init # Init app the first time.
        self.models_meta = []

        if self.init:
            # Build model meta for the first time.
            self._build_models_meta()

    def _build_models_meta(self):
        """
        Create models meta from options.
        """
        model_names = []

        if self.options and self.options.models:
            model_names = self.options.models

        for model_name in model_names:
            model_meta = ModelMeta(model=None)
            model_meta.build_from_name(name=model_name)
            self.models_meta.append(model_meta)

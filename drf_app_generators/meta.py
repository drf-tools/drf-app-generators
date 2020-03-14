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
    min_value = None
    max_value = None

    factory = None

    def __init__(self, django_field=None):
        self.django_field = django_field

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

        # get validators
        for validator in self.django_field.validators:
            if validator.code == 'min_value':
                self.min_value = validator.limit_value
            elif validator.code == 'max_value':
                self.max_value = validator.limit_value


class ModelMeta(object):
    """
    This class holds meta data of a model, attributes,
    and fields.
    """
    model = None # This is Django model.
    name = None # For example: book
    verbose_name_plural = None # For example: books
    object_name = None # the class name of model. Example: Book
    app_label = None # For example: books
    fields = []
    django_fields = []
    abstract = False

    def __init__(self, model=None):
        self.model = model

    def build_from_name(self, name=None):
        """
        Build meta from a model name only.
        This will be called when users generate app from command line.
        """
        self.name = name.lower()
        self.verbose_name_plural = pluralize(self.name)
        self.object_name = self.name.capitalize()
        self.app_label = pluralize(self.name)

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

            # Add factory code
            factory = FactoryMeta(field=field, model=self)
            factory.generate_code()
            field.factory = factory

            self.fields.append(field)

        return self


class FactoryMeta(object):
    """
    Meta data to generate factory for a field.

    Supported field type: Text, CharField, Integer, Float, Boolean.
    """
    code_line = None

    def __init__(self, field=None, model=None):
        self.field = field
        self.model = model

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

    def generate_char_field_code(self):
        # using sequence as default
        self.code_line = '{} = factory.Sequence(lambda n: \'{} {} %03d\' % n)' \
            .format(self.field.name, self.model.object_name, self.field.name)

        print(self.code_line)

    def generate_integer_field_code(self):
        min_value = self.field.min_value if self.field.min_value is not None else 0
        max_value = self.field.max_value if self.field.max_value is not None else 1000

        self.code_line = '{} = factory.fuzzy.FuzzyInteger({}, {})' \
            .format(self.field.name, min_value, max_value)

    def generate_float_field_code(self):
        min_value = self.field.min_value if self.field.min_value is not None else 0.00
        max_value = self.field.max_value if self.field.max_value is not None else 1000.00

        self.code_line = '{} = factory.fuzzy.FuzzyFloat({}, {})' \
            .format(self.field.name, min_value, max_value)

    def generate_boolean_field_code(self):
        self.code_line = '{} = factory.Faker(\'pybool\')' \
            .format(self.field.name)

    def generate_text_field_code(self):
        self.code_line = '{} = factory.Faker(\'sentence\', nb_words=10)' \
            .format(self.field.name)


class AppOptions(object):

    models: [str] = [] # a list of model names
    api_doc: bool = False
    nested: bool = False

    def __init__(self, models=[], api_doc=False, nested=False):
        self.models = models
        self.api_doc = api_doc
        self.nested = nested


class AppConfig(object):
    """
    This contains all configuration to generate/update a Django app.
    """
    name: str = None
    name_capitalized: str = None
    options: AppOptions = AppOptions()
    models_meta: [ModelMeta] = []
    force: bool = False # force to override.

    def __init__(self, name=None, options=None):
        self.name = name
        self.name_capitalized = self.name.capitalize()
        self.options = options

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

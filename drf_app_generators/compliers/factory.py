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
        elif field_type == 'OneToOneField':
            self.generate_one_to_one_code()

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

    def generate_one_to_one_code(self):
        return self.generate_foreign_key_code()

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

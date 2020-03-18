class FieldMeta(object):
    """
    This class holds meta data of a field on model.
    """

    # From django.field
    name: str = None
    attname: str = None # This will be different if it is foreign key.
    primary_key: bool = False
    blank: bool = False
    null: bool = False
    unique: bool = False
    required: bool = False
    choices = None
    default = None
    is_relation: bool = False
    many_to_many: bool = False
    many_to_one: bool = False
    one_to_many: bool = False
    one_to_one: bool = False
    max_length: int = None

    # custom fields
    field_type = None # Get from class of django.field
    field_type_string: str = None

    # from validators
    min_value = None
    max_value = None

    # for Decimal fields
    decimal_places: int = 0
    max_digits: int = 20

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

        if self.blank is False and self.default is None:
            # Mark a field as required
            self.required = True

        if self.field_type_string == 'DecimalField':
            # get decimal attributes
            self.decimal_places = self.django_field.decimal_places
            self.max_digits = self.django_field.max_digits

        if self.field_type_string == 'ForeignKey' \
            or self.field_type_string == 'OneToOneField':
            self.related_model = self.django_field.remote_field.model

        # get validators
        for validator in self.django_field.validators:
            if hasattr(validator, 'code') and validator.code == 'min_value':
                self.min_value = validator.limit_value
            elif hasattr(validator, 'code') and validator.code == 'max_value':
                self.max_value = validator.limit_value

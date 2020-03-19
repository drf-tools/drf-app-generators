from drf_app_generators.helpers import pluralize
from drf_app_generators.compliers.field import FieldMeta
from drf_app_generators.compliers.factory import FactoryMeta


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
    existed: bool = False # Mark that this model is already implemented.

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
        self.existed = False
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
        self.existed = True

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

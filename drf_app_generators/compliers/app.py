from drf_app_generators.compliers.model import ModelMeta


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

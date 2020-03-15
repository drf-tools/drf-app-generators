from django.core.management.base import AppCommand
from drf_app_generators.meta import AppConfig, AppOptions, ModelMeta
from drf_app_generators.generators import (
    FactoryGenerator,
)


class Command(AppCommand):
    help = 'Update the django app based on current settings'

    args = "[appname ...]"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument(
            '--nested',
            action='store_true',
            help='Expand models, apis, factories, serializers to folders',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Expand models, apis, factories, serializers to folders',
        )

    def handle_app_config(self, app_config, **options):
        models = app_config.models
        models_meta = []
        # config = {
        #     'app_name': app_config.name,
        #     'app_name_plural': app_config.name,
        #     'models': models,
        #     'resources': resources, # resources are plural of models, for the apis.
        #     'is_expand': is_expand,
        # }

        # create app config
        app_option = AppOptions(
            nested=options['nested'], force=options['force'])
        app = AppConfig(
            name=app_config.name,
            options=app_option,
            init=False
        )

        for _, model in models.items():
            model_meta = ModelMeta(model=model)
            model_meta.get_meta()

            models_meta.append(model_meta)

        app.models_meta = models_meta

        # Update Factory
        FactoryGenerator(app)

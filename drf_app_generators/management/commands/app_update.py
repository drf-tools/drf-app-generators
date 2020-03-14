from django.core.management.base import AppCommand
from drf_app_generators.meta import ModelMeta


class Command(AppCommand):
    help = 'Update the django app based on current settings'

    args = "[appname ...]"

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

        for key, model in models.items():
            meta = model._meta
            fields = meta.fields

            model_meta = ModelMeta(model=model)
            model_meta.get_meta()

            print(model_meta)

        print(model_meta)

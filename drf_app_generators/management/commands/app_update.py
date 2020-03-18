from django.core.management.base import AppCommand
from drf_app_generators.meta import AppConfig, AppOptions, ModelMeta
from drf_app_generators.generators import (
    AdminGenerator,
    FactoryGenerator,
    ApiGenerator,
    SerializerGenerator,
    UnitTestGenerator,
)


class Command(AppCommand):
    help = 'Update the django app based on current settings'

    args = "[appname ...]"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument(
            '--nested',
            action='store_true',
            help='If you app is using nested folders.',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Override and update all components.',
        )
        parser.add_argument(
            '--factory',
            action='store_true',
            help='Override to update your factories.',
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Override to update your admins.',
        )
        parser.add_argument(
            '--api',
            action='store_true',
            help='Override to update your APIs.',
        )
        parser.add_argument(
            '--serializer',
            action='store_true',
            help='Override to update your serializers.',
        )
        parser.add_argument(
            '--unittest',
            action='store_true',
            help='Override to update your unit test.',
        )

    def handle_app_config(self, app_config, **options):
        print('==============================')
        print(f'Update app: {app_config.name}')

        models = app_config.models
        models_meta: [object] = []

        # create app config
        app_option = AppOptions(
            nested=options['nested'], force=True)
        app = AppConfig(
            name=app_config.name,
            options=app_option,
            init=False
        )

        # Build models meta
        for _, model in models.items():
            model_meta = ModelMeta(model=model)
            models_meta.append(model_meta)

        app.models_meta = models_meta

        # Update the all
        generators: [object] = []

        # Add update generators to execute list.
        if options['factory'] or options['all']:
            generators.append(FactoryGenerator)

        if options['admin'] or options['all']:
            generators.append(AdminGenerator)

        if options['api'] or options['all']:
            generators.append(ApiGenerator)

        if options['serializer'] or options['all']:
            generators.append(SerializerGenerator)

        if options['unittest'] or options['all']:
            generators.append(UnitTestGenerator)

        # Execute the list
        for generator in generators:
            generator(app, update=True)
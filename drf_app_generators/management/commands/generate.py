import sys
import os
from pathlib import Path

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from drf_app_generators.generators import (
    AppFolderGenerator,
    MigrationFolderGenerator,
    TestFolderGenerator,
    ModelGenerator,
    AppConfigGenerator,
    ApiGenerator,
    FactoryGenerator,
    SerializerGenerator,
    AdminGenerator,
    FilterGenerator,
    PermissionGenerator,
    UnitTestGenerator,
    ApidocGenerator,
)
from drf_app_generators.helpers import pluralize


class Command(BaseCommand):
    help = 'Generates DRF apps'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

        parser.add_argument(
            '--models',
            type=str,
            help='List of models you want to generate',
        )
        parser.add_argument(
            '--apidoc',
            action='store_true',
            help='Generate api doc',
        )
        parser.add_argument(
            '--expand',
            action='store_true',
            help='Expand models, apis, factories, serializers to folders',
        )

    def handle(self, *args, **options):
        print('::generate::')
        models = []
        resources = []
        is_expand = False

        if options['models']:
            models = options['models'].split(',')

        if options['expand']:
            is_expand = True

        for model in models:
            resource = {
                'model': model,
                'name': pluralize(model).lower(),
            }
            resources.append(resource)

        app_config = {
            'app_name': options['app_name'],
            'app_name_plural': pluralize(options['app_name']),
            'models': models,
            'resources': resources, # resources are plural of models, for the apis.
            'is_expand': is_expand,
        }

        # Create folders for app.
        AppFolderGenerator(app_config)
        MigrationFolderGenerator(app_config)
        TestFolderGenerator(app_config)
        ModelGenerator(app_config)
        AppConfigGenerator(app_config)
        ApiGenerator(app_config)
        FactoryGenerator(app_config)
        SerializerGenerator(app_config)
        AdminGenerator(app_config)
        UnitTestGenerator(app_config)
        FilterGenerator(app_config)
        PermissionGenerator(app_config)

        if options['apidoc']:
            ApidocGenerator(app_config)

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
from drf_app_generators.meta import AppConfig, AppOptions


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
            '--nested',
            action='store_true',
            help='Expand models, apis, factories, serializers to folders',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Expand models, apis, factories, serializers to folders',
        )

    def handle(self, *args, **options):
        print('::generate::')
        models = []
        nested = False
        apidoc = False
        force = False

        if options['models']:
            models = options['models'].split(',')

        if options['nested']:
            nested = True

        if options['apidoc']:
            apidoc = True

        if options['force']:
            force = True

        app_options = AppOptions(
            models=models, api_doc=apidoc, nested=nested, force=force)
        app_config = AppConfig(name=options['app_name'], options=app_options)

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
        ApidocGenerator(app_config)

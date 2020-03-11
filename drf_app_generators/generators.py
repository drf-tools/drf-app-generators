import os.path
from pathlib import Path
from django.template import Template, Context

from django.conf import settings
from drf_app_generators.templates.models import MODEL_VIEW, MODELS_VIEW
from drf_app_generators.templates.apps import APP_VIEW
from drf_app_generators.templates.apis import API_VIEW, APIS_VIEW
from drf_app_generators.templates.factories import FACTORY_VIEW, FACTORIES_VIEW
from drf_app_generators.templates.serializers import SERIALIZER_VIEW, SERIALIZERS_VIEW
from drf_app_generators.templates.admin import ADMIN_VIEW
from drf_app_generators.templates.filters import FILTER_VIEW
from drf_app_generators.templates.permissions import PERMISSION_VIEW
from drf_app_generators.templates.tests import TEST_MODEL_VIEW, TEST_API_VIEW
from drf_app_generators.templates.apidoc import APIDOC_VIEW


INIT_FILENAME = '__init__.py'


class BaseGenerator(object):
    def __init__(self, app_config, force=False):
        self.app_config = app_config
        self.app_name = app_config['app_name']
        self.app_name_plural = app_config['app_name_plural']
        self.resources = app_config['resources']
        self.is_expand = app_config['is_expand']
        self.force = force
        self.base_dir = os.path.join(os.getcwd())
        self.models = self._get_model_names()

        if settings.BASE_DIR:
            self.base_dir = os.path.join(settings.BASE_DIR)

        self.context = Context({
            'app': self.app_name_plural,
            'app_name': self.app_name, # This is singular app name.
            'models': self.models,
            'resources': self.resources
        })
    #--------------------------------------------------
    # Generate files
    #--------------------------------------------------
    def generate_models(self):
        if self.is_expand:
            self._generate_by_group(group_name='models')
        else:
            self._generate_single_view(name='models')

    def generate_app_config(self):
        content = self.app_config_content()
        filename = 'apps.py'
        self._generate_file_template(filename, content)

    def generate_apis(self):
        if self.is_expand:
            self._generate_by_group(group_name='apis')
        else:
            self._generate_single_view(name='apis')

    def generate_factories(self):
        if self.is_expand:
            self._generate_by_group(group_name='factories')
        else:
            self._generate_single_view(name='factories')

    def generate_serializers(self):
        if self.is_expand:
            self._generate_by_group(group_name='serializers')
        else:
            self._generate_single_view(name='serializers')

    def generate_admin(self):
        content = self.admin_content()
        filename = 'admin.py'
        self._generate_file_template(filename, content)

    def generate_filters(self):
        content = self.filters_content()
        filename = 'filters.py'
        self._generate_file_template(filename, content)

    def generate_permissions(self):
        content = self.permissions_content()
        filename = 'permissions.py'
        self._generate_file_template(filename, content)

    def generate_test_models(self):
        # Create a folder for model tests
        self.create_folder(
            os.path.join(self.base_dir, 'models'),
            init=True,
        )
        for model in self.models:
            content = self.test_model_content(model=model)
            filename = f'models/test_{model.lower()}_models.py'
            self._generate_file_template(filename, content)

    def generate_test_apis(self):
        # Create a folder for model tests
        self.create_folder(
            os.path.join(self.base_dir, 'apis'),
            init=True,
        )
        for model in self.models:
            content = self.test_api_content(model=model)
            filename = f'apis/test_{model.lower()}_apis.py'
            self._generate_file_template(filename, content)

    def generate_tests(self):
        self.generate_test_models()
        self.generate_test_apis()

    def generate_apidoc(self):
        """
        Generate API doc based on template.
        """
        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.create_folder(self.base_dir)

        for resource in self.resources:
            content = self.apidoc_content(resource=resource)
            filename = f'{resource["name"]}.md'
            self._generate_file_template(filename, content)

    #--------------------------------------------------
    # Get contents
    #--------------------------------------------------
    def get_grouping_content(self, resource, view):
        context = self.context
        if resource is not None:
            context = Context({
                'app': self.app_name_plural,
                'resource': resource,
            })
            self.view_template = Template(view)

        return self._view_template_content(context=context)

    def models_content(self, resource=None):
        if resource is not None:
            return self.get_grouping_content(resource=resource, view=MODEL_VIEW)
        return self._view_template_content()

    def app_config_content(self):
        return self._view_template_content()

    def apis_content(self, resource=None):
        if resource is not None:
            return self.get_grouping_content(resource=resource, view=API_VIEW)
        return self._view_template_content()

    def factories_content(self, resource=None):
        if resource is not None:
            return self.get_grouping_content(resource=resource, view=FACTORY_VIEW)
        return self._view_template_content()

    def serializers_content(self, resource=None):
        if resource is not None:
            return self.get_grouping_content(resource=resource, view=SERIALIZER_VIEW)
        return self._view_template_content()

    def serializer_content(self):
        return self._view_template_content()

    def admin_content(self):
        return self._view_template_content()

    def filters_content(self):
        return self._view_template_content()

    def permissions_content(self):
        return self._view_template_content()

    def test_model_content(self, model):
        context = Context({
            'app': self.app_name_plural,
            'model': model,
        })
        self.view_template = Template(TEST_MODEL_VIEW)
        return self._view_template_content(context=context)

    def test_api_content(self, model):
        context = Context({
            'app': self.app_name_plural,
            'model': model,
        })
        self.view_template = Template(TEST_API_VIEW)
        return self._view_template_content(context=context)

    def apidoc_content(self, resource=None):
        context = Context({
            'app': self.app_name_plural,
            'resource': resource,
        })
        self.view_template = Template(APIDOC_VIEW)
        return self._view_template_content(context=context)

    #--------------------------------------------------
    # Internal methods
    #--------------------------------------------------
    def _generate_by_group(self, group_name):
        # Create folder for the group.
        self.create_folder(
            os.path.join(self.base_dir, group_name),
            init=True,
        )
        for resource in self.resources:
            content = getattr(self, f'{group_name}_content')(resource=resource)
            filename = f'{group_name}/{resource["name"]}.py'
            self._generate_file_template(filename, content)

    def _generate_single_view(self, name):
        content = getattr(self, f'{name}_content')()
        filename = f'{name}.py'
        self._generate_file_template(filename, content)

    def _generate_file_template(self, filename, content):
        if filename is None or filename == '':
            return

        return self.write_file(content, filename)

    def _view_template_content(self, context=None):
        if context is None:
            context = self.context

        return self.view_template.render(context)

    def _get_model_names(self):
        return self.app_config['models']

    def create_folder(self, folder_name, force=False, init=False):
        folder_path = os.path.join(self.base_dir, folder_name)
        Path(folder_path).mkdir(parents=False, exist_ok=force)

        if init:
            # create __init__.py file for this folder.
            self.write_file(
                content='',
                filename='__init__.py',
                base_dir=folder_path,
            )

    def write_file(self, content, filename, base_dir=None):
        if base_dir is None:
            base_dir = self.base_dir

        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path) and not self.force:
            msg = f'Are you sure to override {filename} ? (y/n)'
            prompt = input
            response = prompt(msg)
            if response != 'y':
                return False

        new_file = open(file_path, 'w+')
        new_file.write(content)
        new_file.close()
        return True


class AppFolderGenerator(BaseGenerator):
    def __init__(self, app_config, force=False):
        super(AppFolderGenerator, self).__init__(app_config, force)

        self.create_folder(self.app_name_plural)
        self.write_file(
            content='',
            filename=INIT_FILENAME,
            base_dir=os.path.join(self.base_dir, self.app_name_plural),
        )


class MigrationFolderGenerator(BaseGenerator):
    def __init__(self, app_config, force=False):
        super(MigrationFolderGenerator, self).__init__(app_config, force)
        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)

        self.create_folder('migrations')
        self.write_file(
            content='',
            filename=INIT_FILENAME,
            base_dir=os.path.join(self.base_dir, 'migrations'),
        )


class TestFolderGenerator(BaseGenerator):
    def __init__(self, app_config, force=False):
        super(TestFolderGenerator, self).__init__(app_config, force)
        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)

        self.create_folder('tests')
        self.write_file(
            content='',
            filename=INIT_FILENAME,
            base_dir=os.path.join(self.base_dir, 'tests'),
        )


class ModelGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ModelGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(MODELS_VIEW)
        self.generate_models()


class AppConfigGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(AppConfigGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(APP_VIEW)
        self.generate_app_config()


class ApiGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ApiGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(APIS_VIEW)
        self.generate_apis()


class FactoryGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(FactoryGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(FACTORIES_VIEW)
        self.generate_factories()


class SerializerGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(SerializerGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(SERIALIZERS_VIEW)
        self.generate_serializers()


class AdminGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(AdminGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(ADMIN_VIEW)
        self.generate_admin()

class FilterGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(FilterGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(FILTER_VIEW)
        self.generate_filters()


class PermissionGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(PermissionGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural)
        self.view_template = Template(PERMISSION_VIEW)
        self.generate_permissions()


class UnitTestGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(UnitTestGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_name_plural, 'tests')
        self.generate_tests()


class ApidocGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ApidocGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, '../doc')
        self.generate_apidoc()

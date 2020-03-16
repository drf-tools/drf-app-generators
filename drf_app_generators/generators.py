import re
import os.path
from pathlib import Path
from django.template import Template, Context

from django.conf import settings
from drf_app_generators.templates.init import INIT_FILE
from drf_app_generators.templates.models import MODEL_VIEW, MODELS_VIEW, MODEL_INIT
from drf_app_generators.templates.apps import APP_VIEW
from drf_app_generators.templates.apis import API_VIEW, APIS_VIEW, API_INIT
from drf_app_generators.templates.factories import FACTORY_VIEW, FACTORIES_VIEW, FACTORY_INIT
from drf_app_generators.templates.serializers import (
    SERIALIZER_VIEW,
    SERIALIZERS_VIEW,
    SERIALIZER_INIT,
)
from drf_app_generators.templates.admin import ADMIN_VIEW
from drf_app_generators.templates.filters import FILTER_VIEW
from drf_app_generators.templates.permissions import PERMISSION_VIEW
from drf_app_generators.templates.tests import TEST_MODEL_VIEW, TEST_API_VIEW
from drf_app_generators.templates.apidoc import APIDOC_VIEW


INIT_FILENAME = '__init__.py'


class BaseGenerator(object):
    def __init__(self, app_config, force=False):
        self.app_config = app_config
        self.options = app_config.options

        if settings.BASE_DIR:
            self.base_dir = os.path.join(settings.BASE_DIR)

        self.context = Context({
            'app_name': self.app_config.name, # This is singular app name.
            'models': self.app_config.models_meta,
        })

    #--------------------------------------------------
    # Generate files
    #--------------------------------------------------
    def generate_models(self):
        if self.app_config.options.nested:
            # generate init view
            self._generate_by_group(group_name='models', init_view=MODEL_INIT)
        else:
            self._generate_single_view(name='models')

    def generate_app_config(self):
        content = self.app_config_content()
        filename = 'apps.py'
        self._generate_file_template(filename, content)

    def generate_apis(self):
        if self.options.nested:
            self._generate_by_group(
                group_name='apis',
                init_view=API_INIT)
        else:
            self._generate_single_view(name='apis')

    def generate_factories(self):
        if self.options.nested:
            self._generate_by_group(
                group_name='factories',
                init_view=FACTORY_INIT)
        else:
            self._generate_single_view(name='factories')

    def generate_serializers(self):
        if self.options.nested:
            self._generate_by_group(
                group_name='serializers',
                init_view=SERIALIZER_INIT)
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
        for model_meta in self.app_config.models_meta:
            content = self.test_model_content(model_meta=model_meta)
            filename = f'models/test_{model_meta.name}_models.py'
            self._generate_file_template(filename, content)

    def generate_test_apis(self):
        # Create a folder for model tests
        self.create_folder(
            os.path.join(self.base_dir, 'apis'),
            init=True,
        )
        for model_meta in self.app_config.models_meta:
            content = self.test_api_content(model_meta=model_meta)
            filename = f'apis/test_{model_meta.name}_apis.py'
            self._generate_file_template(filename, content)

    def generate_tests(self):
        self.generate_test_models()
        self.generate_test_apis()

    def generate_apidoc(self):
        """
        Generate API doc based on template.
        """
        # Create API docs folder.
        self.create_folder(self.base_dir)

        # Create folder for app.
        self.base_dir = os.path.join(
            self.base_dir, self.app_config.name)

        # Create API docs folder.
        self.create_folder(self.base_dir)

        for model_meta in self.app_config.models_meta:
            content = self.apidoc_content(model_meta=model_meta)
            filename = f'{model_meta.verbose_name_plural}.md'
            self._generate_file_template(filename, content)

    #--------------------------------------------------
    # Get contents
    #--------------------------------------------------
    def get_grouping_content(self, model_meta, view):
        context = self.context
        if model_meta is not None:
            context = Context({
                'app_name': self.app_config.name,
                'model_meta': model_meta,
            })
            self.view_template = Template(view)

        # Templating content
        content = self._view_template_content(context=context)

        # Remove empty lines
        content = re.sub(r'^\n\n', '', content)
        content = re.sub(r'^\n', '', content)
        content = re.sub(r'\n    \n', '\n\n', content)

        return content

    def get_init_content(self, init_view):
        self.view_template = Template(init_view)
        return self._view_template_content()

    def models_content(self, model_meta=None):
        if model_meta is not None:
            return self.get_grouping_content(model_meta=model_meta, view=MODEL_VIEW)
        return self._view_template_content()

    def app_config_content(self):
        return self._view_template_content()

    def apis_content(self, model_meta=None):
        if model_meta is not None:
            return self.get_grouping_content(
                model_meta=model_meta, view=API_VIEW)
        return self._view_template_content()

    def factories_content(self, model_meta=None):
        if model_meta is not None:
            content = self.get_grouping_content(
                model_meta=model_meta, view=FACTORY_VIEW)
            return content
        return self._view_template_content()

    def serializers_content(self, model_meta=None):
        if model_meta is not None:
            return self.get_grouping_content(
                model_meta=model_meta, view=SERIALIZER_VIEW)
        return self._view_template_content()

    def admin_content(self):
        return self._view_template_content()

    def filters_content(self):
        return self._view_template_content()

    def permissions_content(self):
        return self._view_template_content()

    def test_model_content(self, model_meta):
        context = Context({
            'app_name': self.app_config.name,
            'model_meta': model_meta,
        })
        self.view_template = Template(TEST_MODEL_VIEW)
        return self._view_template_content(context=context)

    def test_api_content(self, model_meta):
        context = Context({
            'app_name': self.app_config.name,
            'model_meta': model_meta,
        })
        self.view_template = Template(TEST_API_VIEW)
        return self._view_template_content(context=context)

    def apidoc_content(self, model_meta=None):
        context = Context({
            'app': self.app_config.name,
            'model_meta': model_meta,
        })
        self.view_template = Template(APIDOC_VIEW)
        return self._view_template_content(context=context)

    #--------------------------------------------------
    # Internal methods
    #--------------------------------------------------
    def _generate_by_group(self, group_name, init_view=None):
        # Create folder for the group.
        self.create_folder(
            os.path.join(self.base_dir, group_name),
            init=True if init_view is None else False,
        )

        # Create init file
        if init_view:
            content = self.get_init_content(init_view=init_view)
            self._generate_file_template(
                filename=f'{group_name}/__init__.py', content=content)

        for model_meta in self.app_config.models_meta:
            content = getattr(self, f'{group_name}_content')(model_meta=model_meta)
            filename = f'{group_name}/{model_meta.verbose_name_plural}.py'
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

        if not os.path.exists(folder_path):
            Path(folder_path).mkdir(parents=False, exist_ok=force)

        if init:
            # create __init__.py file for this folder.
            self.write_file(
                content=None,
                filename='__init__.py',
                base_dir=folder_path,
            )

    def write_file(self, content, filename, base_dir=None):
        if base_dir is None:
            base_dir = self.base_dir

        if content is None:
            # Make sure that contain is an empty string if it's None.
            content = str()

        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path) and not self.app_config.options.force:
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

        self.create_folder(self.app_config.name)
        self.write_file(
            content=INIT_FILE,
            filename=INIT_FILENAME,
            base_dir=os.path.join(self.base_dir, self.app_config.name),
        )


class MigrationFolderGenerator(BaseGenerator):
    def __init__(self, app_config, force=False):
        super(MigrationFolderGenerator, self).__init__(app_config, force)
        self.base_dir = os.path.join(self.base_dir, self.app_config.name)

        self.create_folder('migrations', init=True)


class TestFolderGenerator(BaseGenerator):
    def __init__(self, app_config, force=False):
        super(TestFolderGenerator, self).__init__(app_config, force)
        self.base_dir = os.path.join(self.base_dir, self.app_config.name)

        self.create_folder('tests', init=True)


class ModelGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ModelGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(MODELS_VIEW)
        self.generate_models()


class AppConfigGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(AppConfigGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(APP_VIEW)
        self.generate_app_config()


class ApiGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ApiGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(APIS_VIEW)
        self.generate_apis()


class FactoryGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(FactoryGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(FACTORIES_VIEW)
        self.generate_factories()


class SerializerGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(SerializerGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(SERIALIZERS_VIEW)
        self.generate_serializers()


class AdminGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(AdminGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(self.base_dir, self.app_config.name)
        self.view_template = Template(ADMIN_VIEW)
        self.generate_admin()

class FilterGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(FilterGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(
            self.base_dir, self.app_config.name)
        self.view_template = Template(FILTER_VIEW)
        self.generate_filters()


class PermissionGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(PermissionGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(
            self.base_dir, self.app_config.name)
        self.view_template = Template(PERMISSION_VIEW)
        self.generate_permissions()


class UnitTestGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(UnitTestGenerator, self).__init__(app_config, force)

        self.base_dir = os.path.join(
            self.base_dir, self.app_config.name, 'tests')
        self.generate_tests()


class ApidocGenerator(BaseGenerator):

    def __init__(self, app_config, force=False):
        super(ApidocGenerator, self).__init__(app_config, force)

        if self.app_config is not None \
            and self.app_config.options.api_doc:
            self.base_dir = os.path.join(self.base_dir, '../doc')
            self.generate_apidoc()

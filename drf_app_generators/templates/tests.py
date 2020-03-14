__all__ = ['TEST_MODEL_VIEW', 'TEST_API_VIEW']


TEST_MODEL_VIEW = """from django.test import TestCase
from {{ app_name }}.factories import {{ model_meta.object_name }}Factory
from {{ app_name }}.models import {{ model_meta.object_name }}


class {{ model_meta.object_name }}TestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from {{ model_meta.object_name }}Factory
        {{ model_meta.object_name }}Factory()

    def tearDown(self):
        super().tearDown()

        {{ model_meta.object_name }}.objects.all().delete()

    def test_{{ model_meta.name }}_can_be_created(self):
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.first()
        self.assertEqual({{ model_meta.name }}.id, 1)

    def test_{{ model_meta.name }}_can_be_updated(self):
        pass

    def test_{{ model_meta.name }}_can_be_deleted(self):
        pass
"""

TEST_API_VIEW = """from drf_core.tests import BaseTestCase
from {{ app_name }}.factories import {{ model_meta.object_name }}Factory
from {{ app_name }}.models import {{ model_meta.object_name }}
from {{ app_name }}.apis import {{ model_meta.object_name }}ViewSet


class {{ model_meta.object_name }}ViewSetTestCase(BaseTestCase):
    resource = {{ model_meta.object_name }}ViewSet

    def setUp(self):
        super().setUp()

        # Create a {{ model_meta.object_name }} for testing
        {{ model_meta.object_name }}Factory()

    #==============================================================================
    # API should be forbidden if user is not logged in.
    #==============================================================================
    def test_get_{{ model_meta.name }}_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_{{ model_meta.name }}_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_{{ model_meta.name }}_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_{{ model_meta.name }}_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_{{ model_meta.name }}_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()

    #==============================================================================
    # API should be success with authenticated users.
    #==============================================================================
    def test_get_{{ model_meta.name }}_accepted(self):
        self.get_json_ok()

        # Get 1 {{ model_meta.name }}.
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.all()
        self.assertEqual(len({{ model_meta.name }}), 1)

        # Fill in futher test cases

    def test_get_{{ model_meta.name }}_pagination_ok(self):
        self.sampling.generate_by_model(
            app_name='{{ app_name }}',
            model_name='{{ model_meta.object_name }}',
            sampling=100,
        )

        # Get 101 {{ model_meta.verbose_name_plural }}.
        {{ model_meta.verbose_name_plural }} = {{ model_meta.object_name }}.objects.all()
        self.assertEqual(len({{ model_meta.verbose_name_plural }}), 101)

        # Test default case
        resp = self.get_json_ok('', limit=10)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(resp_json['previous'], None)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 10)

        # Test another case
        resp = self.get_json_ok('', limit=25, offset=25)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['previous']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 25)

    def test_post_{{ model_meta.name }}_accepted(self):
        data = {}
        self.post_json_created(data=data)

        # Get 2 {{ model_meta.verbose_name_plural }}.
        {{ model_meta.verbose_name_plural }} = {{ model_meta.object_name }}.objects.all()
        self.assertEqual(len({{ model_meta.verbose_name_plural }}), 2)

        # Fill in futher test cases

    def test_put_{{ model_meta.name }}_accepted(self):
        data = {}
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.first()
        self.put_json_ok(data=data, fragment='%d/' % {{ model_meta.name }}.id)

        # Get 1 {{ model_meta.name }}.
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.all()
        self.assertEqual(len({{ model_meta.name }}), 1)

        # Fill in futher test cases

    def test_delete_{{ model_meta.name }}_accepted(self):
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.first()
        self.delete_json_ok('%d/' % {{ model_meta.name }}.id)

        # Get 0 {{ model_meta.name }}.
        {{ model_meta.name }} = {{ model_meta.object_name }}.objects.non_archived_only()
        self.assertEqual(len({{ model_meta.name }}), 0)

        # Fill in futher test cases
"""
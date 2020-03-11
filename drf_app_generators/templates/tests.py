__all__ = ['TEST_MODEL_VIEW', 'TEST_API_VIEW']


TEST_MODEL_VIEW = """from django.test import TestCase
from {{ app }}.factories import {{ model }}Factory
from {{ app }}.models import {{ model }}


class {{ model }}TestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from {{ model }}Factory
        {{ model }}Factory()

    def tearDown(self):
        super().tearDown()

        {{ model }}.objects.all().delete()

    def test_{{ model|lower }}_can_be_created(self):
        {{ model|lower }} = {{ model }}.objects.first()
        self.assertEqual({{ model|lower }}.id, 1)

    def test_{{ model|lower }}_can_be_updated(self):
        pass

    def test_{{ model|lower }}_can_be_deleted(self):
        pass
"""


TEST_MODELS_VIEW = """from django.test import TestCase

from {{ app }}.factories import ({% for model in models %}
    {{ model }}Factory,{% endfor %}
)

from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)

{% for resource in resources %}
class {{ resource.model }}TestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from {{ resource.model }}Factory
        {{ resource.model }}Factory()

    def tearDown(self):
        super().tearDown()

        {{ resource.model }}.objects.all().delete()

    def test_{{ resource.name }}_can_be_created(self):
        {{ resource.name }} = {{ resource.model }}.objects.first()
        self.assertEqual({{ resource.name }}.id, 1)

    def test_{{ resource.name }}_can_be_updated(self):
        pass

    def test_{{ resource.name }}_can_be_deleted(self):
        pass
{% endfor %}"""


TEST_API_VIEW = """from drf_core.tests import BaseTestCase
from {{ app }}.factories import {{ model }}Factory
from {{ app }}.models import {{ model }}
from {{ app }}.apis import {{ model }}ViewSet


class {{ model }}ViewSetTestCase(BaseTestCase):
    resource = {{ model }}ViewSet

    def setUp(self):
        super().setUp()

        # Create a {{ model }} for testing
        {{ model }}Factory()

    #==============================================================================
    # API should be forbidden if user is not logged in.
    #==============================================================================
    def test_get_{{ model|lower }}_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_{{ model|lower }}_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_{{ model|lower }}_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_{{ model|lower }}_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_{{ model|lower }}_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()

    #==============================================================================
    # API should be success with authenticated users.
    #==============================================================================
    def test_get_{{ model|lower }}_accepted(self):
        self.get_json_ok()

        # Get 1 {{ model|lower }}.
        {{ model|lower }} = {{ model }}.objects.all()
        self.assertEqual(len({{ model|lower }}), 1)

        # Fill in futher test cases

    def test_get_pagination_{{ model|lower }}_ok(self):
        self.sampling.generate_by_model(
            app_name='{{ app }}',
            model_name='{{ model }}',
            sampling=100,
        )

        # Get 101 {{ resource.name }}.
        {{ resource.name }} = {{ model }}.objects.all()
        self.assertEqual(len({{ resource.name }}), 101)

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

    def test_post_{{ model|lower }}_accepted(self):
        data = {}
        self.post_json_created(data=data)

        # Get 2 {{ model|lower }}.
        {{ model|lower }} = {{ model }}.objects.all()
        self.assertEqual(len({{ model|lower }}), 2)

        # Fill in futher test cases

    def test_put_{{ model|lower }}_accepted(self):
        data = {}
        {{ model|lower }} = {{ model }}.objects.first()
        self.put_json_ok(data=data, fragment='%d/' % {{ model|lower }}.id)

        # Get 1 {{ model|lower }}.
        {{ model|lower }} = {{ model }}.objects.all()
        self.assertEqual(len({{ model|lower }}), 1)

        # Fill in futher test cases

    def test_delete_{{ model|lower }}_accepted(self):
        {{ model|lower }} = {{ model }}.objects.first()
        self.delete_json_ok('%d/' % {{ model|lower }}.id)

        # Get 0 {{ model|lower }}.
        {{ model|lower }} = {{ model }}.objects.non_archived_only()
        self.assertEqual(len({{ model|lower }}), 0)

        # Fill in futher test cases
"""
__all__ = ['TEST_MODEL_VIEW', 'TEST_API_VIEW']

TEST_MODEL_VIEW = """from django.test import TestCase

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

TEST_API_VIEW = """from core.tests import BaseTestCase
from {{ app }}.factories import ({% for model in models %}
    {{ model }}Factory,{% endfor %}
)
from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
from {{ app }}.apis import ({% for model in models %}
    {{ model }}ViewSet,{% endfor %}
)
{% for resource in resources %}

class {{ resource.model }}ViewSetTestCase(BaseTestCase):
    resource = {{ resource.model }}ViewSet

    def setUp(self):
        super().setUp()

        # Create a {{ resource.model }} for testing
        {{ resource.model }}Factory()

    #==============================================================================
    # API should be forbidden if user is not logged in.
    #==============================================================================
    def test_get_{{ resource.name }}_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_{{ resource.name }}_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_{{ resource.name }}_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_{{ resource.name }}_forbidden(self):
        self.auth = None
        self.patch_json_forbidden()

    def test_delete_{{ resource.name }}_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()

    #==============================================================================
    # API should be success with authenticated users.
    #==============================================================================
    def test_get_{{ resource.name }}_accepted(self):
        self.get_json_ok()

        # Get 1 {{ resource.model|lower }}.
        {{ resource.name }} = {{ resource.model }}.objects.all()
        self.assertEqual(len({{ resource.name }}), 1)

        # Fill in futher test cases

    def test_post_{{ resource.name }}_accepted(self):
        data = {}
        self.post_json_ok(data=data)

        # Get 2 {{ resource.name }}.
        {{ resource.name }} = {{ resource.model }}.objects.all()
        self.assertEqual(len({{ resource.name }}), 2)

        # Fill in futher test cases

    def test_put_{{ resource.name }}_accepted(self):
        data = {}
        self.put_json_ok(data=data)

        # Get 1 {{ resource.model|lower }}.
        {{ resource.name }} = {{ resource.model }}.objects.all()
        self.assertEqual(len({{ resource.name }}), 1)

        # Fill in futher test cases

    def test_delete_{{ resource.name }}_accepted(self):
        self.delete_json_ok()

        # Get 0 {{ resource.model|lower }}.
        {{ resource.name }} = {{ resource.model }}.objects.all()
        self.assertEqual(len({{ resource.name }}), 0)

        # Fill in futher test cases

{% endfor %}
"""

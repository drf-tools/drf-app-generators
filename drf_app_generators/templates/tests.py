__all__ = ['TEST_MODEL_VIEW', 'TEST_API_VIEW']

TEST_MODEL_VIEW = """from django.test import TestCase

from {{ app }}.factories import ({% for model in models %}
    {{ model }}Factory,{% endfor %}
)

from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)

{% for model in models %}
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
        self.assertEqual(type({{ model|lower }}.id), 1)

    def test_{{ model|lower }}_can_be_updated(self):
        pass

    def test_{{ model|lower }}_can_be_deleted(self):
        pass
{% endfor %}"""

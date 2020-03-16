__all__ = ['FACTORY_VIEW', 'FACTORIES_VIEW', 'FACTORY_INIT']

FACTORIES_VIEW = """import datetime

from drf_core import factories
from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
class {{ model.object_name }}Factory(factories.ModelFactory):
    # Factory data for {{ model.object_name }} model.
    {% for field in model.fields %}{% if field.factory.code_line %}{% autoescape off %}{{ field.factory.code_line }}
    {% endautoescape %}{% endif %}{% endfor %}
    class Meta:
        model = {{ model.object_name }}
{% endfor %}

apps = [{% for model in models %}
    {{ model.object_name }}Factory,{% endfor %}
]
"""

FACTORY_VIEW = """{% for required_lib in model_meta.factory_required_libs %}{{ required_lib }}
{% endfor %}
{% for required_module in model_meta.factory_required_modules %}{{ required_module }}
{% endfor %}
from drf_core import factories
from {{ app_name }}.models.{{ model_meta.verbose_name_plural }} import {{ model_meta.object_name }}


# =============================================================================
# {{ model_meta.object_name }}
# =============================================================================
class {{ model_meta.object_name }}Factory(factories.ModelFactory):
    # Factory data for {{ model_meta.object_name }} model.
    {% for field in model_meta.fields %}{% if field.factory.code_line %}{% autoescape off %}{{ field.factory.code_line }}
    {% endautoescape %}{% endif %}{% endfor %}
    class Meta:
        model = {{ model_meta.object_name }}
"""

FACTORY_INIT = """{% for model in models %}from {{ app_name }}.factories.{{ model.verbose_name_plural }} import {{ model.object_name }}Factory
{% endfor %}

apps = [{% for model in models %}
    {{ model.object_name }}Factory,{% endfor %}
]
"""

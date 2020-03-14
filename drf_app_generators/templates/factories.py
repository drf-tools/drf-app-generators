__all__ = ['FACTORY_VIEW', 'FACTORIES_VIEW', 'FACTORY_INIT']

FACTORIES_VIEW = """from drf_core import factories
from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
class {{ model.object_name }}Factory(factories.ModelFactory):
    # Factory data for {{ model.object_name }} model.

    class Meta:
        model = {{ model.object_name }}
{% endfor %}

apps = [{% for model in models %}
    {{ model.object_name }}Factory,{% endfor %}
]
"""

FACTORY_VIEW = """from drf_core import factories
from {{ app_name }}.models.{{ model_meta.verbose_name_plural }} import {{ model_meta.object_name }}


# =============================================================================
# {{ model_meta.object_name }}
# =============================================================================
class {{ model_meta.object_name }}Factory(factories.ModelFactory):
    # Factory data for {{ model_meta.object_name }} model.

    class Meta:
        model = {{ model_meta.object_name }}


apps = [
    {{ model_meta.object_name }}Factory
]
"""

FACTORY_INIT = """{% for model in models %}from {{ app_name }}.factories.{{ model.verbose_name_plural }} import {{ model.object_name }}Factory
{% endfor %}"""

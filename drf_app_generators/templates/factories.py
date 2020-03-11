__all__ = ['FACTORY_VIEW', 'FACTORIES_VIEW', 'FACTORY_INIT']

FACTORIES_VIEW = """from drf_core import factories
from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model }}
# =============================================================================
class {{ model }}Factory(factories.ModelFactory):
    # Factory data for {{ model }} model.

    class Meta:
        model = {{ model }}
{% endfor %}

apps = [{% for model in models %}
    {{ model }}Factory,{% endfor %}
]
"""

FACTORY_VIEW = """from drf_core import factories
from {{ app }}.models.{{ resource.name }} import {{ resource.model }}


# =============================================================================
# {{ resource.model }}
# =============================================================================
class {{ resource.model }}Factory(factories.ModelFactory):
    # Factory data for {{ resource.model }} model.

    class Meta:
        model = {{ resource.model }}


apps = [
    {{ resource.model }}Factory
]
"""

FACTORY_INIT = """{% for resource in resources %}from {{ app }}.factories.{{ resource.name }} import {{ resource.model }}Factory
{% endfor %}"""

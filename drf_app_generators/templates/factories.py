__all__ = ['FACTORY_VIEW']

FACTORY_VIEW = """from drf_core import factories
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
{% endfor %}"""
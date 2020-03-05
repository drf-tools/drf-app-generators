__all__ = ['FILTER_VIEW']

FILTER_VIEW = """from drf_core.filtering import BaseFiltering
from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model }}
# =============================================================================
class {{ model }}Filtering(BaseFiltering):

    class Meta:
        model = {{ model }}
        exclude = []
{% endfor %}"""

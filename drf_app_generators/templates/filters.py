__all__ = ['FILTER_VIEW']

FILTER_VIEW = """from drf_core.filtering import BaseFiltering
from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
class {{ model.object_name }}Filtering(BaseFiltering):

    class Meta:
        model = {{ model.object_name }}
        exclude = []
{% endfor %}"""

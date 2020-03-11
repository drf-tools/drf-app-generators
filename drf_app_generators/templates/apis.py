__all__ = ['APIS_VIEW', 'API_VIEW', 'API_INIT']

APIS_VIEW = """from drf_core import apis
from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
from {{ app }}.serializers import ({% for model in models %}
    {{ model }}Serializer,{% endfor %}
)
from {{ app }}.filters import ({% for model in models %}
    {{ model }}Filtering,{% endfor %}
)
{% for resource in resources %}

# =============================================================================
# {{ resource.model }}
# =============================================================================
class {{ resource.model }}ViewSet(apis.BaseViewSet):
    # {{ resource.model }} ViewSet

    queryset = {{ resource.model }}.objects.non_archived_only()
    serializer_class = {{ resource.model }}Serializer
    filter_class = {{ resource.model }}Filtering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = '{{ resource.name }}'
{% endfor %}

apps = [{% for resource in resources %}
    {{ resource.model }}ViewSet,{% endfor %}
]
"""

API_VIEW = """from drf_core import apis
from {{ app }}.models import {{ resource.model }}
from {{ app }}.serializers import {{ resource.model }}Serializer
from {{ app }}.filters import {{ resource.model }}Filtering

# =============================================================================
# {{ resource.model }}
# =============================================================================
class {{ resource.model }}ViewSet(apis.BaseViewSet):
    # {{ resource.model }} ViewSet

    queryset = {{ resource.model }}.objects.non_archived_only()
    serializer_class = {{ resource.model }}Serializer
    filter_class = {{ resource.model }}Filtering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = '{{ resource.name }}'

apps = [
    {{ resource.model }}ViewSet,
]
"""

API_INIT = """{% for resource in resources %}from {{ app }}.apis.{{ resource.name }} import {{ resource.model }}ViewSet
{% endfor %}

apps = [{% for resource in resources %}
    {{ resource.model }}ViewSet,{% endfor %}
]
"""

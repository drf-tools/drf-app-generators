__all__ = ['APIS_VIEW', 'API_VIEW', 'API_INIT']

APIS_VIEW = """from drf_core import apis
from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
from {{ app_name }}.serializers import ({% for model in models %}
    {{ model.object_name }}Serializer,{% endfor %}
)
from {{ app_name }}.filters import ({% for model in models %}
    {{ model.object_name }}Filtering,{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
class {{ model.object_name }}ViewSet(apis.BaseViewSet):
    # {{ model.object_name }} ViewSet

    queryset = {{ model.object_name }}.objects.non_archived_only()
    serializer_class = {{ model.object_name }}Serializer
    filter_class = {{ model.object_name }}Filtering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = '{{ model.verbose_name_plural }}'
{% endfor %}

apps = [{% for model in models %}
    {{ model.object_name }}ViewSet,{% endfor %}
]
"""

API_VIEW = """from drf_core import apis
from {{ app_name }}.models import {{ model_meta.object_name }}
from {{ app_name }}.serializers import {{ model_meta.object_name }}Serializer
from {{ app_name }}.filters import {{ model_meta.object_name }}Filtering

# =============================================================================
# {{ model_meta.object_name }}
# =============================================================================
class {{ model_meta.object_name }}ViewSet(apis.BaseViewSet):
    # {{ model_meta.object_name }} ViewSet

    queryset = {{ model_meta.object_name }}.objects.non_archived_only()
    serializer_class = {{ model_meta.object_name }}Serializer
    filter_class = {{ model_meta.object_name }}Filtering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = '{{ model_meta.verbose_name_plural }}'

apps = [
    {{ model_meta.object_name }}ViewSet,
]
"""

API_INIT = """{% for model in models %}from {{ app_name }}.apis.{{ model.verbose_name_plural }} import {{ model.object_name }}ViewSet
{% endfor %}

apps = [{% for model in models %}
    {{ model.object_name }}ViewSet,{% endfor %}
]
"""

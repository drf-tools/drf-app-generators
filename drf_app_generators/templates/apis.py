__all__ = ['API_VIEW']

API_VIEW = """from core import apis
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

    resource_name = {{ resource.name }}
{% endfor %}

apps = [{% for resource in resources %}
    {{ resource.model }}ViewSet,{% endfor %}
]"""

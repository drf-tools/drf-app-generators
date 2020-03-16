__all__ = ['ADMIN_VIEW']

ADMIN_VIEW = """from django.contrib import admin
from drf_core.admin import BaseModelAdmin

from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
@admin.register({{ model.object_name }})
class {{ model.object_name }}Admin(BaseModelAdmin):
    list_display = [{% for field in model.fields %}{% if field.factory.code_line %}
        '{{ field.name }}',{% endif %}{% endfor %}
    ]
{% endfor %}"""
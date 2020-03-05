__all__ = ['ADMIN_VIEW']

ADMIN_VIEW = """from django.contrib import admin
from core.admin import BaseModelAdmin

from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model }}
# =============================================================================
class {{ model }}Admin(BaseModelAdmin):
    pass
{% endfor %}"""
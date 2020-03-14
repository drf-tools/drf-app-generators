__all__ = ['MODEL_VIEW', 'MODELS_VIEW', 'MODEL_INIT']

MODELS_VIEW = """from django.db import models

from drf_core.models import TimeStampedModel, QuerySet
from drf_core import fields
{% for model in models %}

# =============================================================================
# {{ model.object_name }}
# =============================================================================
class {{ model.object_name }}QuerySet(QuerySet):
    pass


class {{ model.object_name }}(TimeStampedModel):

    objects = {{ model.object_name }}QuerySet.as_manager()
{% endfor %}"""

MODEL_VIEW = """from django.db import models

from drf_core.models import TimeStampedModel, QuerySet
from drf_core import fields

# =============================================================================
# {{ model_meta.object_name }}
# =============================================================================
class {{ model_meta.object_name }}QuerySet(QuerySet):
    pass


class {{ model_meta.object_name }}(TimeStampedModel):

    objects = {{ model_meta.object_name }}QuerySet.as_manager()
"""

MODEL_INIT = """{% for model in models %}from {{ app_name }}.models.{{ model.name }} import {{ model.object_name }}
{% endfor %}"""

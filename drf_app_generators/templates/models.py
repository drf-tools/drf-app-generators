__all__ = ['MODEL_VIEW', 'MODELS_VIEW']

MODELS_VIEW = """from django.db import models

from drf_core.models import TimeStampedModel, QuerySet
from drf_core import fields
{% for model in models %}

# =============================================================================
# {{ model }}
# =============================================================================
class {{ model }}QuerySet(QuerySet):
    pass


class {{ model }}(TimeStampedModel):

    objects = {{ model }}QuerySet.as_manager()
{% endfor %}"""

MODEL_VIEW = """from django.db import models

from drf_core.models import TimeStampedModel, QuerySet
from drf_core import fields

# =============================================================================
# {{ resource.model }}
# =============================================================================
class {{ resource.model }}QuerySet(QuerySet):
    pass


class {{ resource.model }}(TimeStampedModel):

    objects = {{ resource.model }}QuerySet.as_manager()
"""

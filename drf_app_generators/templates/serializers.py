__all__ = ['SERIALIZER_VIEW', 'SERIALIZERS_VIEW', 'SERIALIZER_INIT']

SERIALIZERS_VIEW = """from rest_framework import serializers

from {{ app_name }}.models import ({% for model in models %}
    {{ model.object_name }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model.object_name }}Serializer
# =============================================================================
class {{ model.object_name }}Serializer(serializers.ModelSerializer):
    # Serializer for {{ model.object_name }} model.

    class Meta:
        model = {{ model.object_name }}
        fields = '__all__'
{% endfor %}"""

SERIALIZER_VIEW = """from rest_framework import serializers

from {{ app_name }}.models.{{ model_meta.verbose_name_plural }} import {{ model_meta.object_name }}


# =============================================================================
# {{ model_meta.object_name }}Serializer
# =============================================================================
class {{ model_meta.object_name }}Serializer(serializers.ModelSerializer):
    # Serializer for {{ model_meta.object_name }} model.

    class Meta:
        model = {{ model_meta.object_name }}
        fields = '__all__'
"""

SERIALIZER_INIT = """{% for model in models %}from {{ app_name }}.serializers.{{ model.verbose_name_plural }} import {{ model.object_name }}Serializer
{% endfor %}"""

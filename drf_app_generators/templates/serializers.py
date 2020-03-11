__all__ = ['SERIALIZER_VIEW', 'SERIALIZERS_VIEW', 'SERIALIZER_INIT']

SERIALIZERS_VIEW = """from rest_framework import serializers

from {{ app }}.models import ({% for model in models %}
    {{ model }},{% endfor %}
)
{% for model in models %}

# =============================================================================
# {{ model }}Serializer
# =============================================================================
class {{ model }}Serializer(serializers.ModelSerializer):
    # Serializer for {{ model }} model.

    class Meta:
        model = {{ model }}
        fields = '__all__'
{% endfor %}"""

SERIALIZER_VIEW = """from rest_framework import serializers

from {{ app }}.models.{{ resource.name }} import {{ resource.model }}


# =============================================================================
# {{ resource.model }}Serializer
# =============================================================================
class {{ resource.model }}Serializer(serializers.ModelSerializer):
    # Serializer for {{ resource.model }} model.

    class Meta:
        model = {{ resource.model }}
        fields = '__all__'
"""

SERIALIZER_INIT = """{% for resource in resources %}from {{ app }}.serializers.{{ resource.name }} import {{ resource.model }}Serializer
{% endfor %}"""

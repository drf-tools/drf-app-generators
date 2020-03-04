__all__ = ['SERIALIZER_VIEW']

SERIALIZER_VIEW = """from rest_framework import serializers

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

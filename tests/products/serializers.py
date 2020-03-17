from rest_framework import serializers

from products.models import (
    Product,
)


# =============================================================================
# ProductSerializer
# =============================================================================
class ProductSerializer(serializers.ModelSerializer):
    # Serializer for Product model.

    class Meta:
        model = Product
        fields = '__all__'

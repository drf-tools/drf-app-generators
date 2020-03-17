from drf_core.filtering import BaseFiltering
from products.models import (
    Product,
)


# =============================================================================
# Product
# =============================================================================
class ProductFiltering(BaseFiltering):

    class Meta:
        model = Product
        exclude = []

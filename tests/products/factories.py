import datetime

from drf_core import factories
from products.models import (
    Product,
)


# =============================================================================
# Product
# =============================================================================
class ProductFactory(factories.ModelFactory):
    # Factory data for Product model.
    
    class Meta:
        model = Product


apps = [
    ProductFactory,
]

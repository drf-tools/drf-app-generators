from drf_core import apis
from products.models import (
    Product,
)
from products.serializers import (
    ProductSerializer,
)
from products.filters import (
    ProductFiltering,
)


# =============================================================================
# Product
# =============================================================================
class ProductViewSet(apis.BaseViewSet):
    # Product ViewSet

    queryset = Product.objects.non_archived_only()
    serializer_class = ProductSerializer
    filter_class = ProductFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'products'


apps = [
    ProductViewSet,
]

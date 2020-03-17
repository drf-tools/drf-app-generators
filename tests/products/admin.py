from django.contrib import admin
from drf_core.admin import BaseModelAdmin

from products.models import (
    Product,
)


# =============================================================================
# Product
# =============================================================================
@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = [
    ]

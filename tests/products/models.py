from django.db import models
from django.core.validators import MinValueValidator

from drf_core.models import TimeStampedModel, QuerySet
from drf_core import fields
from test_generators.constants import GendersEnum, ColorsEnum, SeasonsEnum, UsagesEnum


# =============================================================================
# Category
# =============================================================================
class CategoryQuerySet(QuerySet):
    pass


class Category(TimeStampedModel):
    """
    Category model
    """
    objects = CategoryQuerySet.as_manager()

    parent = fields.ForeignKey(
        'self',
        verbose_name='Parent category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    name = fields.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.name


# =============================================================================
# Product
# =============================================================================
class ProductQuerySet(QuerySet):
    pass


class Product(TimeStampedModel):
    """
    Product model
    """
    objects = ProductQuerySet.as_manager()
    category = fields.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = fields.CharField(
        max_length=100,
    )
    price = fields.FloatField(
        validators=[MinValueValidator(0)],
    )
    quantity = fields.IntegerField(
        validators=[MinValueValidator(0)],
    )
    sold_quantity = fields.IntegerField(
        validators=[MinValueValidator(0)],
    )
    gender = fields.IntegerField(
        choices=GendersEnum.to_tuple(),
        default=GendersEnum.NA.value,
    )
    base_color = fields.IntegerField(
        choices=ColorsEnum.to_tuple(),
        default=ColorsEnum.NA.value,
    )
    season = fields.IntegerField(
        choices=SeasonsEnum.to_tuple(),
        default=SeasonsEnum.NA.value,
    )
    usage = fields.IntegerField(
        choices=UsagesEnum.to_tuple(),
        default=UsagesEnum.NA.value,
    )
    is_allowed_redeeming = fields.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name

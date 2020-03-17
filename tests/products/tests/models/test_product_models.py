from django.test import TestCase
from products.factories import ProductFactory
from products.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # create data from ProductFactory
        ProductFactory()

    def tearDown(self):
        super().tearDown()

        Product.objects.all().delete()

    def test_product_can_be_created(self):
        product = Product.objects.first()
        self.assertEqual(product.id, 1)

    def test_product_can_be_updated(self):
        pass

    def test_product_can_be_deleted(self):
        pass

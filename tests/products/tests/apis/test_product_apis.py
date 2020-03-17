from drf_core.tests import BaseTestCase
from products.factories import ProductFactory
from products.models import Product
from products.apis import ProductViewSet


class ProductViewSetTestCase(BaseTestCase):
    resource = ProductViewSet

    def setUp(self):
        super().setUp()

        # Create a Product for testing
        ProductFactory()

    #==============================================================================
    # API should be forbidden if user is not logged in.
    #==============================================================================
    def test_get_product_forbidden(self):
        self.auth = None
        self.get_json_method_forbidden()

    def test_post_product_forbidden(self):
        self.auth = None
        data = {}
        self.post_json_method_forbidden(data=data)

    def test_put_product_forbidden(self):
        self.auth = None
        data = {}
        self.put_json_method_forbidden(data=data)

    def test_patch_product_forbidden(self):
        self.auth = None
        data = {}
        self.patch_json_forbidden(data=data)

    def test_delete_product_forbidden(self):
        self.auth = None
        self.delete_method_forbidden()

    #==============================================================================
    # API should be success with authenticated users.
    #==============================================================================
    def test_get_product_accepted(self):
        self.get_json_ok()

        # Get 1 product.
        product = Product.objects.all()
        self.assertEqual(len(product), 1)

        # Fill in futher test cases

    def test_get_product_pagination_ok(self):
        self.sampling.generate_by_model(
            app_name='products',
            model_name='Product',
            sampling=100,
        )

        # Get 101 products.
        products = Product.objects.all()
        self.assertEqual(len(products), 101)

        # Test default case
        resp = self.get_json_ok('', limit=10)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(resp_json['previous'], None)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 10)

        # Test another case
        resp = self.get_json_ok('', limit=25, offset=25)
        resp_json = self.deserialize(resp)

        # Check response JSON
        self.assertEqual(resp_json['count'], 101)
        self.assertEqual(type(resp_json['next']), str)
        self.assertEqual(type(resp_json['previous']), str)
        self.assertEqual(type(resp_json['results']), list)
        self.assertEqual(len(resp_json['results']), 25)

    def test_post_product_accepted(self):
        data = {}
        self.post_json_created(data=data)

        # Get 2 products.
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

        # Fill in futher test cases

    def test_put_product_accepted(self):
        data = {}
        product = Product.objects.first()
        self.put_json_ok(data=data, fragment='%d/' % product.id)

        # Get 1 product.
        product = Product.objects.all()
        self.assertEqual(len(product), 1)

        # Fill in futher test cases

    def test_delete_product_accepted(self):
        product = Product.objects.first()
        self.delete_json_ok('%d/' % product.id)

        # Get 0 product.
        product = Product.objects.non_archived_only()
        self.assertEqual(len(product), 0)

        # Fill in futher test cases

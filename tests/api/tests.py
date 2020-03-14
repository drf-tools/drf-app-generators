import os
import shutil
from django.core.management import call_command
from django.test import TestCase
import time


class GeneratorsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.cwd = os.getcwd()

    def tearDown(self):
        super().tearDown()

        if os.path.exists(os.path.join(self.cwd, 'books')):
            shutil.rmtree(os.path.join(self.cwd, 'books'))
        if os.path.exists(os.path.join(self.cwd, 'foo')):
            shutil.rmtree(os.path.join(self.cwd, 'foo'))
        if os.path.exists(os.path.join(self.cwd, 'bar')):
            shutil.rmtree(os.path.join(self.cwd, 'bar'))

    def test_generate_quick_app(self):
        call_command(
            'generate',
            'books',
            force=True,
        )

        app_folder = os.path.join(self.cwd, 'books')
        self.assertEqual(
            os.path.exists(app_folder), True)
        self.assertEqual(
            os.path.exists(os.path.join(app_folder, 'tests')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, '__init__.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'admin.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'apis.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'apps.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'factories.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'filters.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'permissions.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'models.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'serializers.py')), True
        )

    def test_generate_full_app(self):
        call_command(
            'generate',
            'foo',
            models='Book,Author',
            force=True,
        )

        app_folder = os.path.join(self.cwd, 'foo')
        self.assertEqual(
            os.path.exists(app_folder), True)
        self.assertEqual(
            os.path.exists(os.path.join(app_folder, 'tests')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, '__init__.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'admin.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'apis.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'apps.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'factories.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'filters.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'permissions.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'models.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'serializers.py')), True
        )

    def test_generate_nested_app(self):
        app_folder = os.path.join(self.cwd, 'bar')

        call_command(
            'generate',
            'bar',
            models='Book,Author,Category',
            nested=True,
            force=True,
        )

        self.assertEqual(
            os.path.exists(app_folder), True)
        self.assertEqual(
            os.path.exists(os.path.join(app_folder, 'tests')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, '__init__.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'admin.py')), True
        )
        # API folder exists
        self.assertEqual(
            os.path.exists(
                os.path.join(app_folder, 'apis')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'apis/books.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'apis/authors.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'apis/categories.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'apps.py')), True
        )
        # Factories folder exists
        self.assertEqual(
            os.path.exists(
                os.path.join(app_folder, 'factories')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'factories/books.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'factories/authors.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'factories/categories.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'filters.py')), True
        )
        self.assertEqual(
            os.path.isfile(os.path.join(app_folder, 'permissions.py')), True
        )
        # Models folder exists
        self.assertEqual(
            os.path.exists(
                os.path.join(app_folder, 'models')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'models/books.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'models/authors.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'models/categories.py')
            ),
            True
        )
        # Serializers folder exists
        self.assertEqual(
            os.path.exists(
                os.path.join(app_folder, 'serializers')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'serializers/books.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'serializers/authors.py')
            ),
            True
        )
        self.assertEqual(
            os.path.isfile(
                os.path.join(app_folder, 'serializers/categories.py')
            ),
            True
        )

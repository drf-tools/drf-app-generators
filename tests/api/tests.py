import os
import shutil
from django.core.management import call_command
from django.test import TestCase


class GeneratorsTestCase(TestCase):
    def tearDown(self):
        super().tearDown()
        # shutil.rmtree(os.path.join(os.getcwd(), 'book'))

    def xtest_generate_quick_app(self):
        args = [
            'book',
        ]
        opts = {}

        call_command('generate', *args, **opts)

    def test_generate_full_app(self):
        args = [
            'book',
            '--permission',
            '--models',
            'Book,Author'
        ]
        opts = {}

        call_command('generate', *args, **opts)

from django.core.management import call_command
from django.test import TestCase


class GeneratorsTestCase(TestCase):

    def test_generate_full_app(self):
        args = [
            'book',
            '--models Book,Author',
            '--filter',
            '--permission',
        ]
        opts = {}

        call_command('generate', *args, **opts)

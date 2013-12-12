from django.utils.unittest import TestCase
from drift.importers import Importer
from drift import register


class RegistrationTestCase(TestCase):
    def test_register_sets_metadata(self):
        register(Importer)

        self.assertEqual(Importer.app_label, 'drift')
        self.assertEqual(Importer.module_name, Importer.__name__)

        self.assertEqual(Importer.class_string, 'drift.' + Importer.__name__)

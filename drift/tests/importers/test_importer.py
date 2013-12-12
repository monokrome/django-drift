from django.utils.unittest import TestCase
from drift.importers import Importer


class ImporterTestCase(TestCase):
    """ Tests functionality for importers.Importer. """

    def setUp(self):
        self.importer = Importer()

    def test_match_raises_not_implemented(self):
        def match(): self.importer.match(None)
        self.assertRaises(NotImplementedError, match)

    def test_process_raises_not_implemented(self):
        def process(): self.importer.process(None)
        self.assertRaises(NotImplementedError, process)

    def test_from_string(self):
        self.assertIs(Importer.from_string('drift.Importer'), Importer)

    def test_normalize_header(self):
        self.assertEqual(self.importer.normalize_header(', What?! '), 'what')
        self.assertEqual(self.importer.normalize_header('  WHAT? ', '!'), 'what?')


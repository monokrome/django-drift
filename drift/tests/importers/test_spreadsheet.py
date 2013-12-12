from django.utils.unittest import TestCase

from drift.loaders import ExcelLoader
from drift.tests.mocks import fixtures
from drift.importers import SpreadSheetImporter


class ExampleImporter(SpreadSheetImporter):
    called_process_sheet = 0

    def process_sheet(self, sheet, name, logger):
        self.called_process_sheet += 1


class SpreadSheetImporterTestCase(TestCase):
    def test_get_sheet_list(self):
        loader = ExcelLoader(fixtures['excel'])
        importer = SpreadSheetImporter()

        sheets = importer.get_sheet_list(loader)

        self.assertEqual(len(sheets), 1)
        self.assertEqual(sheets[0], 'Sheet1')

    def test_importer_processes_sheet(self):
        context = fixtures['excel']
        importer = ExampleImporter()

        importer.process(None, context)
        self.assertIs(importer.called_process_sheet, 1)

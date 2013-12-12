from django.utils.unittest import TestCase

from drift.loaders import Loader, ExcelLoader
from drift.tests.mocks import fixtures
from drift.importers import SpreadSheetImporter, ImportFailure


def return_none(*args, **kwargs): return None


class FakeLoader(Loader):
    path = None

    @classmethod
    def sniff(self, *args, **kwargs):
        return None


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

    def test_importer_process_fails_without_loader(self):
        importer = ExampleImporter()

        def process(*args, **kwargs): importer.process(None, fixtures['unknown'])
        self.assertRaises(ImportFailure, process)

    def test_importer_processes_sheet_with_sheets(self):
        context = fixtures['excel']
        importer = ExampleImporter()

        importer.process(None, context)
        self.assertIs(importer.called_process_sheet, 1)

    def test_importer_processes_sheet_without_sheets(self):
        context = fixtures['excel']
        importer = ExampleImporter()

        importer.get_sheet_list = return_none.__get__(ExampleImporter, importer)

        importer.process(None, context)
        self.assertIs(importer.called_process_sheet, 1)

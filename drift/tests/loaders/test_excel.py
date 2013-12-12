from django.utils.unittest import TestCase

from drift.importers import SpreadSheetImporter
from drift.tests.mocks import Fixture
from drift.loaders import ExcelLoader


excel_file = Fixture('excel.xlsx')
csv_file = Fixture('csv_utf8.csv')


class ExcelLoaderTestCase(TestCase):
    def setUp(self):
        self.loader = ExcelLoader(excel_file, autoload=False)

    def test_sniff(self):
        self.assertEqual(ExcelLoader.sniff(excel_file), True)
        self.assertEqual(ExcelLoader.sniff(csv_file), False)

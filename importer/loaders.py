import xlrd
import os

base_loader_error = 'Loader can only be used by extending it.'

excel_extensions = [ '.xls', ]

class Loader(object):
    def __init__(self, file_info):
        self.filename = file_info.path

        self.open()

    def open(self):
        raise NotImplementedError(base_loader_error)

    def close(self):
        pass

    @classmethod
    def sniff(cls, file_info):
        raise NotImplementedError(base_loader_error)

class ExcelLoader(Loader):
    supports_sheets = True
    type_name = 'excel'

    def open(self):
        self.backend = xlrd.open_workbook(self.filename)
        self.sheet_names = self.backend.sheet_names()
        self.sheet_count = len(self.sheet_names)

    def sheet_by_name(self, name):
        """ Returns a sheet based on it's name. """

        return self.backend.sheet_by_name(name)

    def close(self):
        self.backend.release_resources()

    @classmethod
    def sniff(cls, file_info):

        # TODO: Find a way to really sniff the file.
        return os.path.splitext(file_info.path)[-1] in excel_extensions

# TODO: Finish Loader for importing from CSV data.
class CSVLoader(Loader):
    supports_sheets = False

from django.conf import settings

import xlrd
import os


base_loader_error = 'The Loader class can only be used by extending it.'


extensions = getattr(
    settings,
    'DRIFT_LOADER_EXTENSIONS',
    {
        'excel': ('.xls', '.xlsx'),
        'csv': ('csv',)
    }
)


class Loader(object):
    """ Detects and loads data from files. """

    type_name = None

    def __init__(self, context, autoload=True):
        self.filename = context.path

        if autoload is True:
            return self.open()

    def open(self):
        raise NotImplementedError(base_loader_error)

    def close(self):
        pass

    @classmethod
    def sniff(cls, context):
        if not cls.type_name: return False
        if not cls.type_name in extensions: return False

        return os.path.splitext(context.path)[-1] in extensions[cls.type_name]


class ExcelLoader(Loader):
    """ Detects and loads files stored in Excel formats. """

    supports_sheets = True
    type_name = 'excel'

    def open(self):
        self.backend = xlrd.open_workbook(self.filename)
        self.sheet_names = self.backend.sheet_names()
        self.sheet_count = len(self.sheet_names)

    def close(self):
        self.backend.release_resources()

    def sheet_by_name(self, name):
        """ Returns a sheet based on it's name. """

        return self.backend.sheet_by_name(name)


# TODO: Finish Loader for importing from CSV data.
class CSVLoader(Loader):
    """ Detects and loads files stored in CSV format. """

    supports_sheets = False
    type_name = 'csv'

from django.utils.module_loading import module_has_submodule
from django.utils.importlib import import_module
from celery.contrib.methods import task
from django.core.cache import cache
from django.conf import settings

from .loaders import ExcelLoader, CSVLoader
from drift.loaders import Loader


default_queue = getattr(
    settings,
    'DRIFT_DEFAULT_QUEUE',
    'drift'
)


use_cache = getattr(
    settings,
    'DRIFT_IMPORTER_CACHE',
    True
)


not_implemented_error = 'Importer of type {type} does not implement {name}().'


importer_cache_key_format = 'django:importer:from_string:{0}'


class ImportFailure(Exception):
    """ Should be raised in order to indicate a failed import. """

    pass


class Importer(object):
    app_label = None
    module_name = None

    queue = default_queue

    def match(self, context):
        raise NotImplementedError(not_implemented_error.format(
            type=self.__class__.__name__,
            name='match'
        ))

    def process(self, logger, context=None):
        raise NotImplementedError(not_implemented_error.format(
            type=self.__class__.__name__,
            name='process'
        ))

    @classmethod
    def from_string(cls, class_string):
        if use_cache:
            cache_key = importer_cache_key_format.format(class_string)
            cached = cache.get(cache_key)

            if cached:
                return cached

        app_label = class_string[0:class_string.index('.')]
        module_name = class_string[len(app_label)+1:]

        for application in settings.INSTALLED_APPS:
            try:
                found_label = application[application.rindex('.')+1:]
            except ValueError:
                found_label = application

            if found_label == app_label:
                module_reference = import_module(application)

                if module_has_submodule(module_reference, 'importers'):
                    module = import_module(application + '.importers')
                    items_in_module = vars(module)

                    for item_name in items_in_module:
                        if item_name == module_name:
                            result = getattr(module, item_name)
                            if use_cache: cache.set(cache_key, result)

                            return result

    def normalize_header(self, header, ignored_symbols='?!,'):
        """ Normalizes argument string to a more predictable format.

        Normalizes the string passed as 'header' to a more predictable format
        in order to help aid against errors that might exist due to any user
        error in the original spreadsheet.

        By default, this method will perform the following actions:

        * Remove any of the following characters: ?!,
        * Strip any trailing whitespace
        * Convert the entire string to lowercase

        """

        normalized_header = header

        for symbol in ignored_symbols:
            normalized_header = normalized_header.replace(symbol, '')

        normalized_header = normalized_header.strip()
        normalized_header = normalized_header.lower()

        return normalized_header


# TODO: Consider support for Numbers.
class SpreadSheetImporter(Importer):
    """ Imports spreadsheets in Excel & CSV formats.

    """

    type = None
    """ Can be set to a loader class in order to prevent sniffing. """

    # TODO: Modified header map to use multiple sheet's headers.
    header_map = {}
    """ Maps model fields to headers in the spreadsheet. """

    normalize_headers = True
    """ Whether or not spreadsheet headers should be normalized. """

    use_header_map = True
    """ The importer will use the header map when this is set to True. """

    multiple_sheets = True
    """ Specifies how multiple-sheet spreadsheets should be treated.

    Specifies how multiple-sheet spreadsheets should be treated. Possible
    values are:

    * True if all sheets should be used
    * False if only the first sheet should be used
    * A tuple of all sheets by name or zero-based indexes

    """

    spreadsheet_types = {
        ExcelLoader: ['excel'],
    }
    """ List of supported spreadsheet loaders mapped to type names. """

    def get_sheet_list(self, loader):
        if loader.supports_sheets is False:
            return None

        if self.multiple_sheets is False:
            return [0]

        if self.multiple_sheets is True:
            return loader.sheet_names

        return self.multiple_sheets

    def process_sheet(self, sheet, name, logger):
        raise NotImplementedError(not_implemented_error.format(
            type=self.__class__.__name__,
            name='process_name'
        ))

    def process(self, logger, context=None):
        loader = self.type

        if loader is None or isinstance(loader, basestring):
            for loader_class in self.spreadsheet_types:
                if self.type is not None:
                    if self.type not in self.spreadsheet_types[loader_class]:
                        continue

                if loader_class.sniff(context):
                    loader = loader_class(context)

        if loader is None or not isinstance(loader, Loader):
            raise ImportFailure('A loader could not be found for this import.')

        try:
            sheets = self.get_sheet_list(loader)

            if sheets is not None:
                for identifier in sheets:
                    self.process_sheet(identifier, identifier, logger)
            else:
                self.process_sheet(loader, context, logger)

        finally:
            loader.close()


# TODO: DocumentImporter for PDF, Word, Pages, and text files.

from django.utils.module_loading import module_has_submodule
from django.utils.importlib import import_module
from celery.contrib.methods import task
from django.core.cache import cache
from django.conf import settings
from .loaders import ExcelLoader


not_implemented_error = 'Importer of type {type} does not implement {name}().'


class ImportFailure(Exception):
    """ Should be raised in order to indicate a failed import. """

    pass


class Importer(object):
    model = None

    app_label = None
    module_name = None

    def match(self, instance):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='match')

    def process(self, instance, logger):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='process')

    @classmethod
    def from_string(cls, representation):
        cache_key = 'django:importer:from_string:' + representation

        cached = cache.get(cache_key)
        if cached: return cached

        app_label = representation[0:representation.index('.')]
        module_name = representation[len(app_label)+1:]

        for application in settings.INSTALLED_APPS:
            try:
                app_found = application[application.rindex('.')+1:]
            except ValueError:
                app_found = application

            if app_found == app_label:
                module_reference = import_module(application)

                if module_has_submodule(module_reference, 'importers'):
                    module = import_module('{0}.importers'.format(application))

                    # TODO: Not use dir(). Seriously.
                    items_in_module = dir(module)

                    for index in items_in_module:
                        if index.lower() == module_name:
                            result = getattr(module, index)
                            cache.set(cache_key, result)

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

    def process(self, file_info, logger):
        loader = self.type

        if loader is None:
            for loader_class in self.spreadsheet_types:
                if self.type is not None:
                    if self.type not in self.spreadsheet_types[loader]:
                        continue

                if loader_class.sniff(file_info):
                    loader = loader_class(file_info)

        if loader is None:
            raise ImportFailure('A loader could not be found for this import.')

        try:
            sheets = self.get_sheet_list(loader)

            if sheets is not None:
                for identifier in sheets:
                    self.process_sheet(sheet, identifier)
            else:
                self.parse_sheet(loader, identifier)

        finally:
            loader.close()


# TODO: DocumentImporter for PDF, Word, Pages, and text files.

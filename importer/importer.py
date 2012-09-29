not_implemented_error = 'Importer of type {type} does not implement {name}().'

class Importer(object):
    def match(self, file):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='match')

    def process(self, file):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='process')


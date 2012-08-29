from celery.task import Task

not_implemented_error = 'Importer of type {type} does not implement {name}().'

class Importer(Task):
    def match(self, file_handle):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='match')

    def process(self, file_handle):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='process')


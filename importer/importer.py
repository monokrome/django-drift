from django.utils.module_loading import module_has_submodule
from django.utils.importlib import import_module
from .tasks import importer_asynchronous_task
from django.conf import settings

not_implemented_error = 'Importer of type {type} does not implement {name}().'

def get_object_from_module(representation, container_module_name):
    app_label = representation[0:representation.index('.')]
    module_name = representation[len(app_label)+1:]

    for application in settings.INSTALLED_APPS:
        try:
            app_found = application[application.rindex('.')+1:]
        except ValueError:
            app_found = application

        if app_found == app_label:
            module_reference = import_module(application)

            if module_has_submodule(module_reference, container_module_name):
                module = import_module('{0}.{1}'.format(application, container_module_name))

                items_in_module = dir(module)

                for index in items_in_module:
                    if index.lower() == module_name:
                        return getattr(module, index)

class Importer(object):
    model = None

    app_label = None
    module_name = None
    class_string = None

    def match(self, instance):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='match')

    def apply(self, *args, **kwargs):
        importer_asynchronous_task.apply_async(args=args, kwargs=kwargs)

    def process(self, instance, logger=None):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='process'
        )

    @classmethod
    def from_string(cls, representation):
        # TODO: Leverage cached representations once importer.register() supports them.

        return get_object_from_module(representation, 'importers')

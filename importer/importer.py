from django.utils.module_loading import module_has_submodule
from django.utils.importlib import import_module
from celery.contrib.methods import task
from django.conf import settings

not_implemented_error = 'Importer of type {type} does not implement {name}().'

class Importer(object):
    model = None

    app_label = None
    module_name = None

    def match(self, instance):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='match')

    @task
    def run(self, pk):
        instance = self.model.objects.get(pk=pk)

        return self.process(instance)

    def process(self, instance):
        raise NotImplementedError(
            type=not_implemented_error.format(self.__class__.__name__),
            name='process')

    @classmethod
    def from_string(cls, representation):
        # TODO: Leverage cached representations once importer.register() supports them.

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
                            return getattr(module, index)

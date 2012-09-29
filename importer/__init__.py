def autodiscover():
    """ Search for any apps that implement importers and set it up. """

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for application in settings.INSTALLED_APPS:

        module = import_module(application)

        if module_has_submodule(module, 'imports'):
            print(import_module('%s.imports' % application))


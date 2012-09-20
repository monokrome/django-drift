from django.db.models.loading import get_model
from .importers import Importer

def autodiscover():
    """ Search for any apps that implement importers and set it up. """

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for application in settings.INSTALLED_APPS:

        module = import_module(application)

        if module_has_submodule(module, 'importers'):
            import_module('{0}.importers'.format(application))

def register(importer):

    # Don't allow any registration of importers that are not assigned a model
    if importer.model is None:
        raise ValueError('model attribute of {class_name} can not be None.'.format(
            class_name = importer.__class__.__name__
        ))

    # Allow model to be set to a string representation or a direct reference
    if hasattr(importer.model, '__class__') and importer.model.__class__ is str:
        importer.model_string = importer.model
        importer.model = get_model(*importer.model_string.split('.'))

    else:
        importer.model_string = '{app_label}.{module_name}'.format(
            app_label = importer.model._meta.app_label,
            module_name = importer.model._meta.module_name,
        )

    absolute_app_label = str(importer.model.__module__)

    # Remove the last module in the name (IE,
    #   example.app_label.importers becomes example.app_label)
    formatted_app_label = absolute_app_label[0:absolute_app_label.rindex('.')]

    # Remove anything before the last dot if it exists (IE,
    #   example.app_label becomes app_label
    try:
        formatted_app_label = formatted_app_label[formatted_app_label.rindex('.')+1:]
    except ValueError:
        pass

    importer.app_label = formatted_app_label
    importer.module_name = importer.__name__.lower()
    importer.class_string = '{importer.app_label}.{importer.module_name}'.format(
        importer=importer)

    # TODO: Cached representation lookups using Django caching.

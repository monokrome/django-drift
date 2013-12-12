from django.db.models.signals import post_save
from .tasks import drift_task
from django.conf import settings
from .models import Import


import_on_save = getattr(
    settings,
    'IMPORTER_AUTOMATIC',
    'created'
)


def defer_import_execution(sender, instance, **kwargs):
    if not issubclass(sender, Import): return

    if kwargs['created'] is True or import_on_save == 'always':
        instance.status = 'queued'
        instance.save()

        drift_task.apply_async([instance.pk])


if import_on_save is not False:
    post_save.connect(defer_import_execution)

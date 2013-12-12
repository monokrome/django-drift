from celery.utils.log import get_task_logger
from .importers import ImportFailure
from django.db import transaction
from .models import Import
import celery


assuming_failure_message = '{0} did not return True. Assuming failure.'


processing_status = 'processing'
processing_description = 'Processing the data in {filename}.'


success_status = 'success'
success_description = 'The import appears to have completed successfully.'


# The description for failures is the contents of the exception message.
failure_status = 'failure'


# Get the logger for use with this task process
logger = get_task_logger(__name__)


@celery.shared_task
def drift_task(import_pk, *args, **kwargs):
    with transaction.atomic():
        import_instance = Import.objects.get(pk=import_pk).inherited()
        ImportType = import_instance.get_related_importer(**kwargs)

        if ImportType is None:
            import_instance.status = 30
            return False

        importer = ImportType()

        import_instance.status = processing_status
        import_instance.status_description = 'Currently processing file'
        import_instance.save()

        import_context = import_instance.get_context()

        try:
            if importer.process(import_context, logger) is True:
                import_instance.status = success_status
                import_instance.status_description = success_description
                import_instance.save()

            else:
                raise ImportFailure(assuming_failure_message.format(
                    importer.__class__.__name__
                ))

        except ImportFailure, e:
            import_instance.status = failure_status
            import_instance.status_description = e.message
            import_instance.save()

        return True

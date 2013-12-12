from .models import FileImport, statuses
from .importers import ImportFailure
from django.db import transaction
import celery


assuming_failure_message = '{0} did not return True. Assuming failure.'


# TODO: Find a better way to get the tuple values from models.import_statuses
processing_status = 10
processing_description = 'Processing the data in {filename}.'


success_status = 20
success_description = 'The import appears to have completed successfully.'


# The description for failures is the contents of the exception message.
failure_status = 30


@celery.task
@transaction.atomic
def importer_asynchronous_task(uploaded_file_pk, *args, **kwargs):
    logger = importer_asynchronous_task.get_logger()

    import_instance = FileImport.objects.get(pk=uploaded_file_pk)
    importer_class = import_instance.get_related_importer(**kwargs)

    if importer_class is None:
        import_instance.status = 30
        return False

    importer = importer_class()

    import_instance.status = processing_status
    import_instance.status_description = 'Currently processing file'
    import_instance.save()

    file_ref = getattr(import_instance, 'file', None)

    if importer.process(file_ref, logger) is True:
        import_instance.status = success_status
        import_instance.status_description = success_description
        import_instance.save()

    else:
        import_instance.status = failure_status
        import_instance.status_description = e.message
        import_instance.save()

        raise ImportFailure(assuming_failure_message.format(
            importer.__class__.__name__
        ))

    return True

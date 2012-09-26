from .models import ImportedFile
from .importers import ImportFailure
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
def importer_asynchronous_task(uploaded_file_pk, *args, **kwargs):
    logger = importer_asynchronous_task.get_logger()

    imported_file = ImportedFile.objects.get(pk=uploaded_file_pk)
    importer_class = imported_file.get_related_importer(**kwargs)

    if importer_class is None:
        imported_file.status = 30
        return

    importer = importer_class()

    imported_file.status = processing_status
    imported_file.status_description = 'Currently processing file'
    imported_file.save()

    try:
        if importer.process(imported_file.file, logger) is True:
            imported_file.status = success_status
        else:
            raise ImportFailure(assuming_failure_message.format(
                importer.__class__.__name__
            ))

    except ImportFailure, e:
        # TODO: Roll it back.
        imported_file.status = failure_status
        imported_file.status_description = e.message
        imported_file.save()

        return False

    return True

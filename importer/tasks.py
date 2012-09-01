from .models import ImportedFile
import celery

@celery.task
def importer_asynchronous_task(uploaded_file_pk, *args, **kwargs):
    logger = importer_asynchronous_task.get_logger()

    imported_file = ImportedFile.objects.get(pk=uploaded_file_pk)
    importer_class = imported_file.get_related_importer(**kwargs)

    importer = importer_class()
    importer.process(imported_file.file, logger)

    return True

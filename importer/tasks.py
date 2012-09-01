from .models import ImportedFile
import celery

@celery.task
def importer_asyncronous_task(uploaded_file_pk):
    imported_file = ImportedFile.objects.get(pk=uploaded_file_pk)

    model = imported_file.get_related_model()
    importer = imported_file.get_related_importer()

    return True

from django.http import HttpResponse
from django.views.generic import CreateView
from django.db import transaction
from django.http import Http404
from .tasks import importer_asynchronous_task
from .forms import UploadForm
import celery
 
class ImportView(CreateView):
    importers = []

    form_class = UploadForm

    success_url = '/'
    template_name = 'importer/import.html'

    def __init__(self, *args, **kwargs):
        # If a class was passed instead of an instance, then we need to
        # instantiate it first.
        for importer_index in self.importers:
            importer = self.importers[importer_index]

            if importer.__class__ is type:
                self.importers[importer_index] = importer()

        super(ImportView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        instance = form.instance

        for importer in self.importers:
            importer = importer()

            if importer.match(instance):
                # instance.related_model = importer.model
                instance.related_importer = importer.class_string

                result = super(ImportView, self).form_valid(form)

                # Everything is saved and ready to import, so pass
                # this along to celery now.
                importer_asynchronous_task.apply_async([instance.pk])

                return result

        # TODO: Make this pretty.
        raise Http404('No importers support the provided spreadsheet.')

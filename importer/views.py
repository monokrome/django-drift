from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.db.models.loading import get_model
from .forms import UploadForm
from django.db import transaction
import celery
 
@transaction.commit_manually()
class ImportView(View, TemplateResponseMixin):
    template_name = 'importer/import.html'

    model = None
    importers = []

    def __init__(self, *args, **kwargs):
        if hasattr(self.model, '__class__') and self.model.__class__ is str:
            self.model = get_model(*self.model.split('.'))

        super(ImportView, self).__init__(*args, **kwargs)

    def get(self, request):
        form = UploadForm()

        context = {
            'form': form,
            'view': self,
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']

        for importer in self.importers:
            if importer.match(file):
                return importer.process(file)

        return HttpResponse('DERP DE DERP')


from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from .forms import UploadForm
 
class ImportView(View, TemplateResponseMixin):
    template_name = 'importer/import.html'

    model = None
    importers = []

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


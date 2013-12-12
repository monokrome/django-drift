from django.db.models.loading import get_model
from django.db import models
import importer


class Import(models.Model):
    related_importer = models.CharField(max_length=64)

    status = models.CharField(max_length=32, default='created')
    status_description = models.TextField(max_length=128, null=True, blank=True)

    def get_related_model(self):
        return get_model(*self.related_model.split('.'))

    def get_related_importer(self):
        return importer.Importer.from_string(self.related_importer)

    def get_context(self):
        return None


class FileImport(Import):
    file = models.FileField(upload_to='imports')

    def get_context(self):
        return self.file

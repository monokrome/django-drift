from django.db.models.loading import get_model
from django.db import models
import importer


class Import(models.Model):
    related_importer = models.CharField(max_length=64)

    status = models.CharField(max_length=32, default='created')
    status_description = models.TextField(max_length=128, null=True, blank=True)

    def get_related_importer(self):
        return importer.Importer.from_string(self.related_importer)

    def get_context(self):
        return None

    def inherited(self):
        for attribute in dir(self):
            value = getattr(self, attribute)
            is_inherited = isinstance(value, self.__class__)

            if is_inherited and value.import_ptr.pk == self.pk:
                return value

        return self

class FileImport(Import):
    file = models.FileField(upload_to='imports')

    def get_context(self):
        return self.file

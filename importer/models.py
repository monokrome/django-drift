from django.db.models.loading import get_model
from django.db import models
import importer

import_statuses = (
        (0,  'queued'),
        (10, 'processing'),
        (20, 'completed'),
        (30, 'failed'),
)

class ImportedFile(models.Model):
    file = models.FileField(upload_to='imports')
    status = models.PositiveIntegerField(max_length=3, default=0)

    related_model = models.CharField(max_length=128)
    related_importer = models.CharField(max_length=128)

    status_description = models.CharField(max_length=128, null=True)

    def get_related_model(self):
        return get_model(*self.related_model.split('.'))

    def get_related_importer(self):
        return importer.Importer.from_string(self.related_importer)

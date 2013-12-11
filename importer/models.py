from django.db.models.loading import get_model
from django.conf import settings
from django.db import models
import importer


statuses = getattr(
    settings,
    'IMPORTER_STATUSES',
    (
        (0,  'queued'),
        (10, 'processing'),
        (20, 'success'),
        (30, 'failure'),
    )
)


class Import(models.Model):
    related_model = models.CharField(max_length=128)
    related_importer = models.CharField(max_length=128)

    status_description = models.CharField(max_length=128, null=True)
    status = models.PositiveIntegerField(
        max_length=3,
        default=0,
        choices=statuses
    )

    def get_related_model(self):
        return get_model(*self.related_model.split('.'))

    def get_related_importer(self):
        return importer.Importer.from_string(self.related_importer)


class ImportedFile(models.Model):
    file = models.FileField(upload_to='imports')

from django import forms
from .models import ImportedFile

class UploadForm(forms.ModelForm):
    class Meta(object):
        model = ImportedFile
        fields = (
            'file',
        )

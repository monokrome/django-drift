from django import forms
from .models import FileImport


class UploadForm(forms.ModelForm):
    class Meta(object):
        model = FileImport
        fields = (
            'file',
        )

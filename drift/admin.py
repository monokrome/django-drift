from django.contrib import admin
from .models import Import, FileImport


class ImportAdmin(admin.ModelAdmin):
    readonly_fields = (
        'status_description',
        'status',
    )


admin.site.register(Import, ImportAdmin)
admin.site.register(FileImport, ImportAdmin)

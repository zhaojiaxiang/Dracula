from django.contrib import admin

from qa.models import QaDetail


@admin.register(QaDetail)
class QaDetailAdmin(admin.ModelAdmin):
    list_display = ('fcontent', 'fclass1', 'fsortrule', 'fregression', 'fapproval', 'fresult')


from rest_framework import viewsets

from checkouts.models import CheckOutFiles
from checkouts.serializers import CheckOutFilesSerializer


class CheckOutFilesViewSet(viewsets.ModelViewSet):
    serializer_class = CheckOutFilesSerializer

    def get_queryset(self):
        return CheckOutFiles.objects.all()

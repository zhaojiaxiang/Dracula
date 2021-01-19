from rest_framework import viewsets

from systems.models import Systems
from systems.serializers import SystemsSerializer


class SystemsViewSet(viewsets.ModelViewSet):
    serializer_class = SystemsSerializer

    def get_queryset(self):
        return Systems.objects.all()

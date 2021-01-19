from rest_framework import viewsets

from projects.models import Projects
from projects.serializers import ProjectsSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return Projects.objects.all()

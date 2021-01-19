from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from liaisons.models import Liaisons
from reports.filters import ReportLiaisonsFilter
from reports.serializers import ReportLiaisonSerializer


class ReportListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Liaisons.objects.distinct().values('fsystemcd', 'fprojectcd', 'fodrno').all()
    serializer_class = ReportLiaisonSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReportLiaisonsFilter
    ordering_fields = ['fodrno']
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from checkouts.filters import CheckOutFilesFilter
from checkouts.models import CheckOutFiles
from checkouts.serializers import CheckOutFilesSerializer


class CheckOutFilesPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CheckOutFilesViewSet(viewsets.ModelViewSet):
    serializer_class = CheckOutFilesSerializer
    pagination_class = CheckOutFilesPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = CheckOutFilesFilter

    def get_queryset(self):
        return CheckOutFiles.objects.all().order_by('fchkstatus', 'fslipno', '-fregisterdte')

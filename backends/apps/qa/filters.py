import django_filters

from qa.models import QaHead, QaDetail


class QaHeadFilter(django_filters.rest_framework.FilterSet):
    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    ftype = django_filters.CharFilter(field_name='ftype',  lookup_expr='contains')
    fstatus = django_filters.CharFilter(field_name='fstatus', lookup_expr='exact')
    fobjectid = django_filters.CharFilter(field_name='fobjectid', lookup_expr='exact')

    class Meta:
        model = QaHead
        fields = ("fslipno", "ftype", "fstatus", "fobjectid")


class QaDetailFilter(django_filters.rest_framework.FilterSet):
    qahf = django_filters.CharFilter(field_name='qahf__id', lookup_expr='contains')

    class Meta:
        model = QaDetail
        fields = ("qahf", )

import django_filters

from liaisons.models import Liaisons


class LiaisonsFilter(django_filters.rest_framework.FilterSet):
    """
    Liaison的过滤类
    """
    fsystemcd = django_filters.CharFilter(field_name='fsystemcd',  lookup_expr='exact')
    fprojectcd = django_filters.CharFilter(field_name='fprojectcd', lookup_expr='exact')
    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    ftype = django_filters.CharFilter(field_name='ftype',  lookup_expr='contains')
    fstatus = django_filters.CharFilter(field_name='fstatus', lookup_expr='exact')
    fodrno = django_filters.CharFilter(field_name='fodrno', lookup_expr='contains')
    fleader = django_filters.CharFilter(field_name='fleader', lookup_expr='contains')
    fhelper = django_filters.CharFilter(field_name='fhelper',  lookup_expr='contains')
    fassignedto = django_filters.CharFilter(field_name='fassignedto',  lookup_expr='contains')
    fsirno = django_filters.CharFilter(field_name='fsirno',  lookup_expr='contains')
    fgroups = django_filters.CharFilter(field_name='fgroups',lookup_expr='contains')

    class Meta:
        model = Liaisons
        fields = ['fsystemcd', 'fprojectcd', 'fslipno', 'ftype', 'fstatus', 'fodrno', 'fleader', 'fhelper',
                  'fassignedto', 'fsirno', 'fgroups']

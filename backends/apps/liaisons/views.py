from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from liaisons.filters import LiaisonsFilter
from liaisons.models import Liaisons
from liaisons.serializers import LiaisonsSerializer, LiaisonUpdateStatusSerializer, QaProjectSerializer
from qa.models import QaHead, QaDetail


class LiaisonsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LiaisonsViewSet(viewsets.ModelViewSet):
    # queryset = Liaisons.objects.all().order_by('fstatus', '-fcreatedte')
    serializer_class = LiaisonsSerializer
    pagination_class = LiaisonsPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = LiaisonsFilter
    ordering_fields = ['fstatus', 'fcreatedte']

    def get_queryset(self):
        return Liaisons.objects.filter(fassignedto=self.request.user.name).order_by('fstatus', '-fcreatedte')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if instance.fstatus != "1":
                data = {
                    'code': '400',
                    'message': '只有初始状态下才可以删除'
                }
                return Response(data, status=status.HTTP_200_OK)

            if instance.ftype == "追加开发":
                qahf = QaHead.objects.filter(fslipno__exact=instance.fslipno).first()
                qadf = QaDetail.objects.filter(qahf=qahf)
                if qadf:
                    data = {
                        'code': '400',
                        'message': '已经存在测试用例，不可删除'
                    }
                    return Response(data, status=status.HTTP_200_OK)

            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                'code': '500',
                'message': str(e)
            }
            return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic()
    def perform_destroy(self, instance):
        order_no = instance.fodrno
        instance.delete()
        liaison = Liaisons.objects.filter(fodrno__exact=order_no)
        qahf = QaHead.objects.filter(fslipno__exact=order_no)
        if qahf and not liaison:
            qahf.delete()


class LiaisonUpdateStatusViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                                 mixins.UpdateModelMixin, GenericViewSet):
    queryset = Liaisons.objects.all()
    serializer_class = LiaisonUpdateStatusSerializer


class QaProjectForGroupViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    本组项目明细ViewSet
    """
    def get_queryset(self):
        user = self.request.user
        return Liaisons.objects.values("fodrno").filter(fgroups__ammic_group__exact=user.ammic_group.id).distinct()

    serializer_class = QaProjectSerializer


class QaProjectForMineViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    与本人相关的项目明细ViewSet
    """
    def get_queryset(self):
        user = self.request.user
        return Liaisons.objects.values("fodrno").filter(Q(fassignedto__exact=user.name) |
                                                        Q(fleader__contains=user.name) |
                                                        Q(fhelper__contains=user.name)).distinct()

    serializer_class = QaProjectSerializer


class QaProjectViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    所有项目明细ViewSet
    """
    def get_queryset(self):
        return Liaisons.objects.values("fodrno").distinct()

    serializer_class = QaProjectSerializer

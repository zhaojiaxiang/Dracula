from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response

from qa.filters import QaHeadFilter, QaDetailFilter
from qa.models import QaHead, QaDetail
from qa.serializers import QaHeadSerializer, QaDetailSerializer, QaDetailUpdateResultSerializer, \
    QaDetailUpdateContentTextSerializer, QaHeadUpdateObjectSummarySerializer, QaHeadModifyDetailSerializer


class MCLQaHeadViewSet(viewsets.ModelViewSet):
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaHeadFilter
    ordering_fields = ['fstatus', '-fcreatedte']

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qa_detail = QaDetail.objects.filter(qahf__exact=instance)
            if instance.fstatus != "1":
                data = {
                    'code': '400',
                    'message': '只有初始状态下才可以删除'
                }
                return Response(data, status=status.HTTP_200_OK)
            elif qa_detail:
                data = {
                    'code': '400',
                    'message': '已经存在测试项不可删除'
                }
                return Response(data, status=status.HTTP_200_OK)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                'code': '500',
                'message': str(e)
            }
            return Response(data, status=status.HTTP_200_OK)


class QaHeadUpdateObjectSummaryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet):
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadUpdateObjectSummarySerializer


class QaHeadModifyDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadModifyDetailSerializer


class MCLQaDetailViewSet(viewsets.ModelViewSet):
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailFilter
    ordering_fields = ['fsortrule']


class MCLQaDetailUpdateResultViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateResultSerializer


class MCLQaDetailUpdateContentTextViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                          viewsets.GenericViewSet):
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateContentTextSerializer



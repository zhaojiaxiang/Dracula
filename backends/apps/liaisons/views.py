import os
import uuid

from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from liaisons.filters import LiaisonsFilter
from liaisons.models import Liaisons
from liaisons.serializers import LiaisonsSerializer, LiaisonUpdateStatusSerializer, QaProjectSerializer
from qa.models import QaHead, QaDetail
from utils.db_connection import query_single_with_no_parameter, db_connection_execute
from utils.utils import create_folder


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


class QaProjectDetailView(APIView):

    def get(self, request):
        order_no = request.GET.get('order_no')
        sql_str = f"""
                    select liaisonf.id           slip_id,
                           liaisonf.fslipno      slip_slip,
                           liaisonf.fstatus      slip_status,
                           liaisonf.fbrief       slip_brief,
                           liaisonf.fassignedto  slip_assignedto,
                           liaisonf.fplnstart    slip_plnstart,
                           liaisonf.fplnend      slip_plnend,
                           liaisonf.factstart    slip_actstart,
                           liaisonf.factend      slip_actend,
                           liaisonf.freleasedt   slip_release,
                           liaisonf.fplnmanpower slip_plnmanpower,
                           liaisonf.factmanpower slip_actmanpower,
                           design.id             design_id,
                           qahf.id               qa_id,
                           qahf.fobjectid        qa_object,
                           qahf.fstatus          qa_status,
                           qahf.fobjmodification qa_modification,
                           code.id               code_id
                    from qahf
                             left join codereview code 
                             on code.fslipno = qahf.fslipno and code.fobjectid = qahf.fobjectid,
                         liaisonf
                             left join codereview design 
                             on design.fslipno = liaisonf.fslipno and design.fobjectid = 'Design Review'
                    where fodrno = '{order_no}'
                      and liaisonf.fslipno = qahf.fslipno
                    order by liaisonf.fslipno;
                  """

        project_detail = db_connection_execute(sql_str, 'dict')
        return Response(data=project_detail, status=status.HTTP_200_OK)


class LiaisonFileUpload(APIView):
    def post(self, request):

        orig_file = request.FILES.get('file')

        extension = orig_file.name.split('.')[1].lower()

        file_name = str(uuid.uuid4()) + '.' + extension

        upload_path = os.path.join("media/upload/file", file_name[0], file_name[1])

        create_folder(upload_path)

        file_path = os.path.join(upload_path, file_name)

        # file_path
        with open(file_path, 'wb') as f:
            for i in orig_file.chunks():
                f.write(i)

        if 'liaison' in request.data:
            file_path = os.path.join(file_name[0], file_name[1], file_name)
            liaison_id = request.data['liaison']
            liaison = Liaisons.objects.get(pk=liaison_id)
            liaison.freleaserpt = file_path
            liaison.save()

        return Response(status=status.HTTP_200_OK)

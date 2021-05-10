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

from accounts.models import User
from backends.settings import SLIMS_STATUS
from liaisons.filters import LiaisonsFilter, QAProjectFilter, QAProjectDataStatisticsFilter
from liaisons.models import Liaisons
from liaisons.serializers import LiaisonsSerializer, LiaisonUpdateStatusSerializer, QaProjectSerializer, \
    QaProjectDataStatisticsSerializer
from qa.models import QaHead, QaDetail
from utils.db_connection import query_single_with_no_parameter, db_connection_execute
from utils.slims import SLIMSExchange
from utils.utils import create_folder, get_all_organization_group_belong_me


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


class AllLiaisonsViewSet(viewsets.ModelViewSet):
    """
    LiaisonsViewSet是个人的所有联络票号接口
    AllLiaisonsViewSet是所有的联络票接口
    """
    queryset = Liaisons.objects.all().order_by('fstatus', '-fcreatedte')
    serializer_class = LiaisonsSerializer


class LiaisonUpdateStatusViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                                 mixins.UpdateModelMixin, GenericViewSet):
    queryset = Liaisons.objects.all()
    serializer_class = LiaisonUpdateStatusSerializer


class QaProjectForGroupPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


class QaProjectForGroupViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    本组项目明细ViewSet
    """

    def get_queryset(self):
        all_group_tuple = get_all_organization_group_belong_me(self.request)
        # 此处没有对数据进行排序，因为不好排，前端获取到该数据后会进行排序
        return Liaisons.objects.values("fodrno", "forganization").filter(
            forganization__in=all_group_tuple).distinct().order_by('-fodrno')

    serializer_class = QaProjectSerializer
    pagination_class = QaProjectForGroupPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QAProjectFilter


class QaProjectForMineViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    与本人相关的项目明细ViewSet
    """

    def get_queryset(self):
        user = self.request.user
        return Liaisons.objects.values("fodrno", "forganization").filter(Q(fassignedto__exact=user.name) |
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


class QaProjectDataStatisticsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    订单下联络票的测试数据统计
    """
    def get_queryset(self):
        return Liaisons.objects.values("fslipno", "fassignedto").distinct().order_by('fslipno')

    serializer_class = QaProjectDataStatisticsSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QAProjectDataStatisticsFilter


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


class SyncLiaisonBySirNo(APIView):

    def get(self, request):
        try:
            sir_no = request.GET.get('sync_sirno')

            liasons = Liaisons.objects.filter(fsirno__exact=sir_no)

            if liasons:
                data = {
                    'code': '400',
                    'message': f"Sir No:{sir_no}已经绑定联络票号，不可同步！"
                }
                return Response(data, status.HTTP_200_OK)

            results = None
            if SLIMS_STATUS:
                slims = SLIMSExchange(request)
                results = slims.sync_slims(sir_no)

            if results:
                sir_no_list = results[0]

                sir_status = sir_no_list[0]
                sir_dateopened = sir_no_list[1]
                sir_openedby = sir_no_list[2]
                sir_assignedto = sir_no_list[3]
                sir_odrno = sir_no_list[10]
                sir_prjno = sir_no_list[11]
                sir_category = sir_no_list[12]
                sir_productid = sir_no_list[13]
                sir_jpmodules = sir_no_list[14]
                sir_jpdescription = sir_no_list[15]

                if sir_jpdescription:
                    sir_jpdescription = sir_jpdescription.strip()
                if sir_jpmodules:
                    sir_jpmodules = sir_jpmodules.strip()

                sir_status = sir_status.strip()
                sir_category = sir_category.strip()
                if sir_status == 'O':
                    ...
                elif sir_status == 'R':
                    ...
                elif sir_status == 'F':
                    data = {
                        'code': '400',
                        'message': f"Sir No:{sir_no}已完成，不可同步！"
                    }
                    return Response(data, status.HTTP_200_OK)
                elif sir_status == 'C':
                    data = {
                        'code': '400',
                        'message': f"Sir No:{sir_no}已关闭，不可同步！"
                    }
                    return Response(data, status.HTTP_200_OK)
                else:
                    data = {
                        'code': '400',
                        'message': f"Sir No:{sir_no}状态异常！"
                    }
                    return Response(data, status.HTTP_200_OK)

                ftype = ""
                if sir_category == "REQ":
                    ftype = "追加开发"
                elif sir_category == "EHM":
                    ftype = "改善需求"
                elif sir_category == "BUG":
                    ftype = "维护阶段障碍"

                openedby = User.objects.get(slmsname__exact=sir_openedby)
                fcreateusr = openedby.name
                assignedto = User.objects.get(slmsname__exact=sir_assignedto)
                fassignedto = assignedto.name

                data = {'ftype': ftype, 'fcreateusr': fcreateusr, 'fcreatedte': sir_dateopened,
                        "fplnstart": sir_dateopened, 'fassignedto': fassignedto, 'fsystemcd': sir_productid.strip(),
                        'fprojectcd': sir_prjno.strip(), 'fodrno': sir_odrno.strip(), 'fbrief': sir_jpmodules,
                        'fcontent': sir_jpdescription, 'fsirno': sir_no}

                return Response(data, status.HTTP_200_OK)
            else:
                data = {
                    'code': '400',
                    'message': "无法同步数据，请输入正确的Sir No!"
                }
                return Response(data=data, status=status.HTTP_200_OK)

        except Exception as ex:
            data = {
                'code': '400',
                'message': str(ex)
            }
            return Response(data=data, status=status.HTTP_200_OK)

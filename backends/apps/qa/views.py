import os
import uuid

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from liaisons.models import Liaisons
from qa.filters import QaHeadFilter, QaDetailFilter
from qa.models import QaHead, QaDetail
from qa.serializers import MCLQaHeadSerializer, QaDetailSerializer, QaDetailUpdateResultSerializer, \
    QaDetailUpdateContentTextSerializer, QaHeadUpdateObjectSummarySerializer, QaHeadModifyDetailSerializer, \
    QaHeadTargetAndActualSerializer
from utils.utils import create_folder


class MCLQaHeadViewSet(viewsets.ModelViewSet):
    queryset = QaHead.objects.order_by('fstatus', '-fcreatedte')
    serializer_class = MCLQaHeadSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaHeadFilter
    # ordering_fields = ['fstatus', '-fcreatedte']

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


class QaHeadTargetAndActualViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = QaHead.objects.all()
    serializer_class = QaHeadTargetAndActualSerializer


class MCLQaDetailViewSet(viewsets.ModelViewSet):
    queryset = QaDetail.objects.all().order_by('fsortrule', 'fclass1', 'fregression')
    serializer_class = QaDetailSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailFilter
    # ordering_fields = ['fsortrule']


class MCLQaDetailUpdateResultViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                     viewsets.GenericViewSet):
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateResultSerializer


class MCLQaDetailUpdateContentTextViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                          viewsets.GenericViewSet):
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateContentTextSerializer


class ImageUpload(APIView):

    def post(self, request):
        image = request.FILES.get('file')

        extension = image.name.split('.')[1].lower()

        image_name = str(uuid.uuid4()) + '.' + extension

        upload_path = os.path.join("media/upload/image", image_name[0], image_name[1])

        create_folder(upload_path)

        image_path = os.path.join(upload_path, image_name)

        # 保存单个文件
        with open(image_path, 'wb') as f:
            for i in image.chunks():
                f.write(i)

        ret_url = os.path.join(request.stream._current_scheme_host, image_path)

        ret = {"code": 0, "msg": "success", "data": {"url": ret_url}}
        return Response(data=ret, status=status.HTTP_200_OK)


class FileUpload(APIView):

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

        ret_url = os.path.join(request.stream._current_scheme_host, file_path)

        ret_path = f'<p><a href="{ret_url}">{orig_file}</a></p>'

        data = {"path": ret_path}

        if 'liaison' in request.data:
            file_path = os.path.join("upload/file", file_name[0], file_name[1], file_name)
            liaison_id = request.data['liaison']
            liaison = Liaisons.objects.get(pk=liaison_id)
            liaison.freleaserpt = file_path
            liaison.save()

            ret_url = os.path.join(request.stream._current_scheme_host, "media", file_path)
            data['liaison'] = ret_url

        return Response(data=data, status=status.HTTP_200_OK)

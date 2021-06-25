import datetime
import os
import uuid

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, filters
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sendfile import sendfile

from qa.filters import QaHeadFilter, QaDetailFilter, QaDetailProofFilter
from qa.models import QaHead, QaDetail, Qadfproof
from qa.serializers import QaHeadSerializer, QaDetailSerializer, QaDetailUpdateResultSerializer, \
    QaDetailUpdateContentTextSerializer, QaHeadUpdateObjectSummarySerializer, QaHeadModifyDetailSerializer, \
    QaHeadTargetAndActualSerializer, PCLQaClass1Serializer, PCLQaClass2Serializer, \
    QaDetailApprovalContentTextSerializer, QadfproofContentTextSerializer
from reviews.models import CodeReview
from utils.utils import create_folder, regex_content


class MCLQaHeadViewSet(viewsets.ModelViewSet):
    """
    MCL测试对象增删改查 API
    包含：排序、过滤
    """
    queryset = QaHead.objects.order_by('fstatus', '-fslipno2', '-fcreatedte')
    serializer_class = QaHeadSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaHeadFilter

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
            else:
                if qa_detail:
                    data = {
                        'code': '400',
                        'message': '已经存在测试项不可删除'
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    if instance.ftesttyp == "PCL":
                        qa_count = QaHead.objects.filter(fslipno__exact=instance.fslipno).count()
                        if qa_count == 1:
                            data = {
                                'code': '400',
                                'message': '至少要存在一条PCL数据'
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
    """
    测试对象 概要 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadUpdateObjectSummarySerializer


class QaHeadModifyDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    测试对象 修改明细 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadModifyDetailSerializer


class QaHeadTargetAndActualViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    测试对象 测试目标 API
    """
    queryset = QaHead.objects.all()
    serializer_class = QaHeadTargetAndActualSerializer


class QaDetailViewSet(viewsets.ModelViewSet):
    """
    测试明细表 增删改查 API
    """
    queryset = QaDetail.objects.all().order_by('fsortrule', 'fclass1', 'fclass2', 'fregression', '-pk')
    serializer_class = QaDetailSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailFilter


class QaDetailUpdateResultViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    测试项结果 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateResultSerializer


class QaDetailUpdateContentTextViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet):
    """
    测试项贴图 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateContentTextSerializer


class QaDetailApprovalContentTextViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                         viewsets.GenericViewSet):
    """
    测试项评论贴图，提交测试结果后，检查测试项时评论功能 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailApprovalContentTextSerializer


class QadfProofContentTextViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """

    """
    queryset = Qadfproof.objects.all().order_by('-id')
    serializer_class = QadfproofContentTextSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailProofFilter


class PCLQaClass1ViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    PCL 以分类1进行分组展示数据 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='PCL')
    serializer_class = PCLQaClass1Serializer


class PCLQaClass2ViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    PCL 以分类1 + 分类2进行分组展示数据 API
    """
    serializer_class = PCLQaClass2Serializer

    def get_queryset(self):
        qahf = self.request.GET.get('qahf_id')
        class1 = self.request.GET.get('class1')
        queryset = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1).values('qahf_id',
                                                                                              'fclass1').distinct()
        return queryset


class ReFormatContentText(APIView):
    """
    由于CKeditor4和CKeditor5生成的数据格式不同，为了向上兼容，可使用该接口重置旧数据
    注：上线时使用，其余不可使用
    """
    def get(self, request):
        model = request.GET.get("model")
        data = {
            "code": 200,
            "message": model + "数据格式化成功"
        }
        try:
            proofs = ''
            if model == "qadf":
                proofs = QaDetail.objects.filter(fcontent_text__isnull=False)
            elif model == "proof":
                proofs = Qadfproof.objects.all()

            for proof in proofs:
                content_text = proof.fcontent_text
                proof.fcontent_text = regex_content(content_text)
                proof.save()
        except Exception as ex:
            data = {
                "code": 400,
                "message": model + str(ex)
            }
        return Response(data, status=status.HTTP_200_OK)


class PCLCommitJudgment(APIView):

    def get(self, request):
        qahf_id = request.GET.get('qahf')
        qahead = QaHead.objects.filter(pk=qahf_id)
        qa_status = qahead[0].fstatus
        qa_result = 'OK'
        qadetail = QaDetail.objects.filter(qahf_id__exact=qahf_id).values('fresult').distinct()
        for qa in qadetail:
            if qa['fresult'] == 'NG':
                qa_result = 'NG'
                break
            elif qa['fresult'] is None:
                qa_result = 'NG'
                break

        data = {'status': qa_status, 'result': qa_result}
        return Response(data=data, status=status.HTTP_200_OK)


class TestResultDefaultOK(APIView):
    """
    MCL和PCL列表中，点击Default OK按钮，将该测试对象下所有未录入结果的测试项默认设置为 “OK”
    """

    def put(self, request):
        data = {}
        user = request.user
        try:
            qahf_id = request.data['qahf']
            qa_details = QaDetail.objects.filter(qahf_id=qahf_id)
            for detail in qa_details:
                if detail.fresult is None:
                    detail.fresult = 'OK'
                    detail.ftestusr = user.name
                    detail.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
                    detail.save()
        except Exception as e:
            data = {
                'code': '500',
                'message': str(e)
            }
        return Response(data, status=status.HTTP_200_OK)


class CodeReviewInspection(APIView):

    def get(self, request):
        data = {}
        object_id = request.GET.get('object_id')
        slip_no = request.GET.get('slip_no')

        code_review = CodeReview.objects.filter(fobjectid__exact=object_id,
                                                fslipno__exact=slip_no)
        if code_review.count() == 0:
            data = {
                'code': '400',
                'message': '代码Review没填写'
            }
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class RecoverFile(APIView):
    """
    富文本编辑器文件展示处理API
    """

    def get(self, request, filename):
        ret_url = os.path.join("media/upload/image", filename[0], filename[1], filename)

        return sendfile(request, filename=ret_url, attachment=True)


class CkEditorImageUpload(APIView):
    """
    富文本编辑器图片上传API
    """

    def post(self, request):
        image = request.FILES.get('file')

        extension = image.name.split('.')[1].lower()

        image_name = str(uuid.uuid4()) + '.' + extension

        upload_path = os.path.join("media/upload/image", image_name[0], image_name[1])

        create_folder(upload_path)

        image_save_path = os.path.join(upload_path, image_name)

        # 保存单个文件
        with open(image_save_path, 'wb') as f:
            for i in image.chunks():
                f.write(i)

        ret_url = os.path.join("files", image_name)

        ret = {"code": 0, "msg": "success", "data": {"url": ret_url}}
        return Response(data=ret, status=status.HTTP_200_OK)


class CkEditorFileUpload(APIView):
    """
    富文本编辑器文件上传API
    """

    def post(self, request):
        orig_file = request.FILES.get('file')

        extension = orig_file.name.split('.')[1].lower()

        file_name = "T" + str(uuid.uuid4()) + '.' + extension

        upload_path = os.path.join("media/upload/image", file_name[0], file_name[1])

        create_folder(upload_path)

        file_path = os.path.join(upload_path, file_name)

        # file_path
        with open(file_path, 'wb') as f:
            for i in orig_file.chunks():
                f.write(i)

        ret_url = os.path.join('files', file_name)

        ret_path = f'<p><a href="{ret_url}">{orig_file}</a></p>'

        data = {"path": ret_path}

        # if 'liaison' in request.data:
        #     file_path = os.path.join("upload/file", file_name[0], file_name[1], file_name)
        #     liaison_id = request.data['liaison']
        #     liaison = Liaisons.objects.get(pk=liaison_id)
        #     liaison.freleaserpt = file_path
        #     liaison.save()
        #
        #     ret_url = os.path.join(request.stream._current_scheme_host, "media", file_path)
        #     data['liaison'] = ret_url

        return Response(data=data, status=status.HTTP_200_OK)

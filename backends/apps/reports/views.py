from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from liaisons.models import Liaisons
from reports.filters import ReportLiaisonsFilter
from reports.serializers import ReportLiaisonSerializer, ReportLiaisonListSerializer
from reports.utils import get_liaison_with_list, get_qa_with_list


class ReportListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Liaisons.objects.distinct().values('fsystemcd', 'fprojectcd', 'fodrno').all()
    serializer_class = ReportLiaisonSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReportLiaisonsFilter


class ReportLiaisonListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Liaisons.objects.filter(fstatus__in=('3', '4')).order_by('fslipno')
    serializer_class = ReportLiaisonListSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReportLiaisonsFilter


class ReportLiaisonInfo(APIView):

    def get(self, request):
        slip_no = request.GET.get('slip_no')
        liaison_list = get_liaison_with_list(slip_no)
        return Response(liaison_list, status=status.HTTP_200_OK)


class ReportQaInfo(APIView):

    def get(self, request):
        slip_no = request.GET.get('slip_no')
        image = request.GET.get('image')
        qa_list = get_qa_with_list(slip_no, image)
        return Response(qa_list, status=status.HTTP_200_OK)


class ReportOrderInfo(APIView):

    def get(self, request):

        order_list = []
        slip_list = []
        order_no = request.GET.get('order_no')
        multiple_slip = request.GET.get('multiple_slip')
        if multiple_slip:
            slip_list = multiple_slip.split(",")
        image = request.GET.get('image')
        liaisons = Liaisons.objects.filter(fodrno__exact=order_no, fstatus__in=('3', '4')).order_by('fslipno')
        for liaison in liaisons:
            liaison_dict = {}
            if multiple_slip:
                if liaison.fslipno in slip_list:
                    liaison_dict['liaison'] = get_liaison_with_list(liaison.fslipno)
                    liaison_dict['qa'] = get_qa_with_list(liaison.fslipno, image)
                    order_list.append(liaison_dict)
            else:
                liaison_dict['liaison'] = get_liaison_with_list(liaison.fslipno)
                liaison_dict['qa'] = get_qa_with_list(liaison.fslipno, image)
                order_list.append(liaison_dict)

        return Response(order_list, status=status.HTTP_200_OK)

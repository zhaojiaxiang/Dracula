from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import SystemSetting
from accounts.serializers import UserSerializer, SystemSettingSerializer, MyGroupUserSerializer
from utils.db_connection import db_connection_execute, query_single_with_no_parameter

User = get_user_model()


def jwt_response_payload_handler(token, user=None, request=None):
    """
    设置jwt登录之后返回token和user信息
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class MyGroupUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MyGroupUserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True, ammic_group=self.request.user.ammic_group)


class SystemSettingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer


class UserDevelopmentDetail(APIView):

    def get(self, request, format=None):
        current_username = request.user.name

        all_not_release_order_sql = f"""
                                   select distinct fodrno from liaisonf 
                                   where (fassignedto = '{current_username}' or fhelper like '{current_username}' 
                                   or fleader like '{current_username}') and ftype = '追加开发' and fstatus <> 5"""

        all_not_release_orders = db_connection_execute(all_not_release_order_sql)

        response_data = []

        for order in all_not_release_orders:
            order_no = order[0]

            order_partner_sql = f"select fassignedto, fleader, fhelper from liaisonf where fodrno = '{order_no}'"
            order_partner_result = db_connection_execute(order_partner_sql)

            user_tuple = ()
            for order_partner_tuple in order_partner_result:
                user_tuple = user_tuple + order_partner_tuple

            user_list = []
            user_tuple = set(user_tuple)
            for username in user_tuple:
                if len(username) > 0:
                    if "," in username:
                        split_list = username.split(",")
                        user_list = user_list + split_list
                    else:
                        user_list.append(username)
            user_list = list(set(user_list))
            order_partner = len(user_list)

            order_slipno_all_sql = f"select count(*) from liaisonf where fodrno = '{order_no}'"
            order_slipno_all_list = query_single_with_no_parameter(order_slipno_all_sql, "list")
            order_slipno_all = order_slipno_all_list[0]

            order_slipno_close_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus in ('3', '4', '5')"
            order_slipno_close_list = query_single_with_no_parameter(order_slipno_close_sql, "list")
            order_slipno_close = order_slipno_close_list[0]

            order_slipno_release_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 5 "
            order_slipno_release_list = query_single_with_no_parameter(order_slipno_release_sql, "list")
            order_slipno_release = order_slipno_release_list[0]

            order_slipno_working_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 2"
            order_slipno_working_list = query_single_with_no_parameter(order_slipno_working_sql, "list")
            order_slipno_working = order_slipno_working_list[0]

            order_slipno_init_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 1"
            order_slipno_init_list = query_single_with_no_parameter(order_slipno_init_sql, "list")
            order_slipno_int = order_slipno_init_list[0]

            test_object_sql = f"select count(*) from qahf where fslipno in (select fslipno from liaisonf where fodrno = '{order_no}')"
            test_object_list = query_single_with_no_parameter(test_object_sql, "list")
            test_object = test_object_list[0]

            order_note_sql = f"select fnote from qahf where ftesttyp = 'PCL' and fslipno = '{order_no}'"
            order_note_list = query_single_with_no_parameter(order_note_sql, "list")

            order_note = "******"
            if order_note_list:
                order_note = order_note_list[0]

            order_status = 1
            if order_slipno_working > 0 or \
                    (order_slipno_working == 0 and order_slipno_close > 0 and order_slipno_close != order_slipno_all):
                order_status = 2
            elif order_slipno_working == 0 and order_slipno_close == order_slipno_all:
                order_status = 3
            elif order_slipno_release == order_slipno_all:
                order_status = 4

            order_dict = {}

            order_dict['order_no'] = order_no
            order_dict['order_note'] = order_note
            order_dict['order_partner'] = order_partner
            order_dict['order_slipno_all'] = order_slipno_all
            order_dict['order_slipno_close'] = order_slipno_close
            order_dict['order_slipno_working'] = order_slipno_working + order_slipno_int
            order_dict['test_object'] = test_object
            order_dict['order_status'] = order_status

            response_data.append(order_dict)

        return Response(data=response_data, status=status.HTTP_200_OK)


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    data = {}
    if response is not None:
        data = {
            'code': response.status_code,
            'message': response.reason_phrase
        }
        if hasattr(exc, 'detail'):
            data['message'] = exc.detail[0]

    return Response(data=data, status=status.HTTP_200_OK)

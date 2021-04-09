from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import SystemSetting
from accounts.serializers import UserSerializer, SystemSettingSerializer, MyGroupUserSerializer, LoginSerializer
from liaisons.models import Liaisons
from qa.models import QaHead
from utils.db_connection import db_connection_execute, query_single_with_no_parameter
from utils.utils import get_all_organization_belong_me, get_all_organization_group_belong_me

User = get_user_model()


@permission_classes((AllowAny,))
class LoginView(APIView):
    """
    自定义用户登录
    """
    def post(self, request):
        # 实例化得到一个序列化类的对象
        serializer = LoginSerializer(data=request.data,)
        # 序列化类的对象的校验方法
        serializer.is_valid(raise_exception=True)
        token = serializer.context.get('token')
        user = serializer.context.get('user')
        # 如果通过,表示登录成功,返回手动签发的token
        # 如果失败,抛异常,就不用管了
        data = {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
        return Response(data, status.HTTP_200_OK)


def jwt_response_payload_handler(token, user=None, request=None):
    """
    设置jwt登录之后返回token和user信息
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


def api_exception_handler(exc, context):
    """
    自定义异常返回接口格式
    :param exc:
    :param context:
    :return:
    """
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
            if response.status_code != status.HTTP_400_BAD_REQUEST:
                data['message'] = exc.detail
            else:
                try:
                    data['message'] = exc.detail[0]
                except Exception as e:
                    data['message'] = exc.detail[list(exc.detail)[0]][0]

    return Response(data=data, status=status.HTTP_200_OK)


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
                                   select distinct fodrno, fprojectcd from liaisonf 
                                   where (fassignedto = '{current_username}' or fhelper like '{current_username}' 
                                   or fleader like '{current_username}') and ftype = '追加开发' and fstatus <> 4 """

        all_not_release_orders = db_connection_execute(all_not_release_order_sql)

        response_data = []

        for order in all_not_release_orders:
            order_no = order[0]
            project = order[1]

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

            order_slipno_close_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 3"
            order_slipno_close_list = query_single_with_no_parameter(order_slipno_close_sql, "list")
            order_slipno_close = order_slipno_close_list[0]

            order_slipno_release_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 4 "
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
            order_dict['project'] = project

            response_data.append(order_dict)

        return Response(data=response_data, status=status.HTTP_200_OK)


class MyTaskBar(APIView):

    def get(self, request):
        user = request.user

        mcl = QaHead.objects.filter(fcreateusr__exact=user.name,
                                    fstatus__exact='2',
                                    ftesttyp__exact='MCL').count()

        pcl = QaHead.objects.filter(fslipno__in=Liaisons.objects.values('fodrno').filter(fleader__contains=user.name),
                                    fstatus__in=(1, 2),
                                    ftesttyp__exact='PCL').count()

        all_organization_tuple = get_all_organization_belong_me(request)

        approval_sql = f"""
                       select count(*)
                            from (
                                 select distinct qahf.id  qahf_id,
                                     qahf.ftesttyp,
                                     liaisonf.fodrno,
                                     liaisonf.fslipno,
                                     qahf.fobjectid,
                                     qahf.fstatus,
                                     qahf.fobjmodification,
                                     (select codereview.id
                                      from codereview
                                      where codereview.fobjectid = qahf.fobjectid
                                        and codereview.fslipno = qahf.fslipno) code_id,
                                     (select codereview.id
                                      from codereview
                                      where codereview.fobjectid = 'Design Review'
                                        and codereview.fslipno = qahf.fslipno) design_id
                                 from liaisonf,
                                      qahf,
                                      qadf
                                 where qadf.qahf_id = qahf.id
                                   and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                                   and qahf.fcreateusr in (select name from users where ammic_organization_id 
                                   in {all_organization_tuple})
                                   and qadf.fapproval = 'N'
                                   and qahf.ftesttyp = 'MCL'
                                   and qahf.fstatus in ('1', '2')
                                 union all
                                 select distinct qahf.id,
                                                 qahf.ftesttyp,
                                                 qahf.fslipno,
                                                 qahf.fslipno2 fslipno,
                                                 qahf.fobjectid,
                                                 qahf.fstatus,
                                                 qahf.fnote,
                                                 ''            code_id,
                                                 ''            design_id
                                 from qahf,
                                      qadf,
                                      liaisonf
                                 where ftesttyp = 'PCL'
                                   and qahf.id = qadf.qahf_id
                                   and qadf.fapproval = 'N'
                                   and qahf.fstatus in ('1', '2')
                                   and liaisonf.fodrno = qahf.fslipno
                                   and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in 
                                   (select name from users where ammic_organization_id in {all_organization_tuple}))) a
                            order by ftesttyp, fodrno, fslipno
                      """

        approval_list = query_single_with_no_parameter(approval_sql, 'list')
        approval = approval_list[0]

        confirm_sql = f"""
                      select count(*)
                        from (
                                 select qahf.id                                   qahf_id,
                                        qahf.ftesttyp,
                                        liaisonf.fodrno,
                                        liaisonf.fslipno,
                                        qahf.fobjectid,
                                        qahf.fstatus,
                                        qahf.fobjmodification,
                                        (select codereview.id
                                         from codereview
                                         where codereview.fobjectid = qahf.fobjectid
                                           and codereview.fslipno = qahf.fslipno) code_id,
                                        (select codereview.id
                                         from codereview
                                         where codereview.fobjectid = 'Design Review'
                                           and codereview.fslipno = qahf.fslipno) design_id
                                 from liaisonf,
                                      qahf
                                 where (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                                   and qahf.fcreateusr in (select name from users where ammic_organization_id in {all_organization_tuple})
                                   and qahf.fstatus = '3'
                                   and qahf.ftesttyp = 'MCL'
                                 union all
                                 select distinct qahf.id,
                                                 qahf.ftesttyp,
                                                 qahf.fslipno,
                                                 qahf.fslipno2 fslipno,
                                                 qahf.fobjectid,
                                                 qahf.fstatus,
                                                 qahf.fnote,
                                                 ''            code_id,
                                                 ''            design_id
                                 from qahf,
                                      liaisonf
                                 where qahf.ftesttyp = 'PCL'
                                   and qahf.fstatus = '3'
                                   and liaisonf.fodrno = qahf.fslipno
                                   and liaisonf.fleader like '%{user.name}%') a
                      """
        confirm_list = query_single_with_no_parameter(confirm_sql, 'list')
        confirm = confirm_list[0]

        all_organization_group_tuple = get_all_organization_group_belong_me(request)

        dev_count_sql = f"""
                        select count(*)
                            from (
                                 select qahf_c.fslipno, count(*) count
                                 from (
                                      select distinct fslipno, fstatus
                                      from qahf
                                      where fslipno in (
                                          select fslipno
                                          from liaisonf
                                          where fodrno in (
                                              select fslipno
                                              from qahf
                                              where fslipno in (
                                                  select qahf_b.fslipno
                                                  from (select fslipno, count(*) count
                                                        from (select fslipno, fstatus from qahf 
                                                        where ftesttyp = 'PCL') qahf_a
                                                        group by fslipno) qahf_b
                                                  where qahf_b.count = 1)
                                                and fstatus = '4')
                                            and liaisonf.fstatus = '3' and 
                                            liaisonf.forganization in {all_organization_group_tuple})) qahf_c
                                 group by qahf_c.fslipno) a
                            where a.count = 1
                        """

        dev_count_list = query_single_with_no_parameter(dev_count_sql, 'list')
        dev_count = dev_count_list[0]

        non_dev_count_sql = f"""
                            select count(*)
                                from (
                                     select a.fslipno, a.fstatus, count(*) count
                                     from (
                                          select distinct qahf.fslipno, qahf.fstatus
                                          from liaisonf,
                                               qahf
                                          where liaisonf.fslipno = qahf.fslipno
                                            and liaisonf.ftype <> '追加开发'
                                            and liaisonf.fstatus = '3'
                                            and liaisonf.forganization in {all_organization_group_tuple}) a
                                     group by a.fslipno, a.fstatus) b
                                where b.count = 1
                                  and b.fstatus = '4';
                                """

        non_dev_count_list = query_single_with_no_parameter(non_dev_count_sql, 'list')
        non_dev_count = non_dev_count_list[0]

        release = dev_count + non_dev_count

        response_data = []
        task_dict = {}

        task_dict['mcl'] = mcl
        task_dict['pcl'] = pcl
        task_dict['approval'] = approval
        task_dict['confirm'] = confirm
        task_dict['release'] = release

        response_data.append(task_dict)

        return Response(data=response_data, status=status.HTTP_200_OK)


class MyMcl(APIView):

    def get(self, request):
        user = request.user

        mcl_sql = f"""
                   select
                   liaisonf.id,
                   liaisonf.fslipno,
                   liaisonf.fodrno,
                   qahf.id qahf_id,
                   qahf.fobjectid,
                   qahf.fstatus,
                   qahf.ftesttyp,
                   qahf.fobjmodification,
                   (select codereview.id from codereview where 
                        codereview.fobjectid = qahf.fobjectid and codereview.fslipno = qahf.fslipno) code_id,
                   (select codereview.id from codereview where 
                        codereview.fobjectid = 'Design Review' and codereview.fslipno = qahf.fslipno) design_id
                   from qahf,
                        liaisonf
                   where qahf.fstatus = '2'
                        and qahf.fcreateusr = '{user.name}'
                        and qahf.ftesttyp = 'MCL'
                        and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                   order by liaisonf.fodrno, liaisonf.fslipno
                  """

        mcl_dict = db_connection_execute(mcl_sql, 'dict')

        return Response(data=mcl_dict, status=status.HTTP_200_OK)


class MyPcl(APIView):

    def get(self, request):
        user = request.user

        pcl_sql = f"""
                   select distinct
                       qahf.id    qahf_id,
                       liaisonf.fodrno,
                       qahf.fslipno2 fslipno,
                       qahf.fnote fobjmodification,
                       qahf.fobjectid,
                       qahf.ftesttyp,
                       qahf.fstatus,
                       ''         design_id,
                       ''         code_id
                   from liaisonf,
                         qahf
                   where liaisonf.fodrno = qahf.fslipno
                      and liaisonf.ftype = '追加开发'
                      and liaisonf.fleader like '%{user.name}%'
                      and qahf.ftesttyp = 'PCL'
                      and qahf.fstatus in (1, 2)
                    order by qahf.fstatus, liaisonf.fodrno
                  """

        pcl_dict = db_connection_execute(pcl_sql, 'dict')

        return Response(data=pcl_dict, status=status.HTTP_200_OK)


class MyApproval(APIView):

    def get(self, request):
        user = request.user

        all_organization_tuple = get_all_organization_belong_me(request)

        approval_sql = f"""
                       select *
                            from (
                                 select distinct qahf.id  qahf_id,
                                     qahf.ftesttyp,
                                     liaisonf.fodrno,
                                     liaisonf.fslipno,
                                     qahf.fobjectid,
                                     qahf.fstatus,
                                     qahf.fobjmodification,
                                     (select codereview.id
                                      from codereview
                                      where codereview.fobjectid = qahf.fobjectid
                                        and codereview.fslipno = qahf.fslipno) code_id,
                                     (select codereview.id
                                      from codereview
                                      where codereview.fobjectid = 'Design Review'
                                        and codereview.fslipno = qahf.fslipno) design_id
                                 from liaisonf,
                                      qahf,
                                      qadf
                                 where qadf.qahf_id = qahf.id
                                   and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                                   and qahf.fcreateusr in (select name from users where ammic_organization_id 
                                   in {all_organization_tuple})
                                   and qadf.fapproval = 'N'
                                   and qahf.ftesttyp = 'MCL'
                                   and qahf.fstatus in ('1', '2')
                                 union all
                                 select distinct qahf.id,
                                                 qahf.ftesttyp,
                                                 qahf.fslipno,
                                                 qahf.fslipno2 fslipno,
                                                 qahf.fobjectid,
                                                 qahf.fstatus,
                                                 qahf.fnote,
                                                 ''            code_id,
                                                 ''            design_id
                                 from qahf,
                                      qadf,
                                      liaisonf
                                 where ftesttyp = 'PCL'
                                   and qahf.id = qadf.qahf_id
                                   and qadf.fapproval = 'N'
                                   and qahf.fstatus in ('1', '2')
                                   and liaisonf.fodrno = qahf.fslipno
                                   and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in 
                                   (select name from users where ammic_organization_id in {all_organization_tuple}))) a
                            order by ftesttyp, fodrno, fslipno
                      """

        approval_dict = db_connection_execute(approval_sql, 'dict')

        return Response(data=approval_dict, status=status.HTTP_200_OK)


class MyConfirm(APIView):

    def get(self, request):
        user = request.user

        all_organization_tuple = get_all_organization_belong_me(request)

        confirm_sql = f"""
                       select qahf.id                                   qahf_id,
                               qahf.ftesttyp,
                               liaisonf.fodrno,
                               liaisonf.fslipno,
                               qahf.fobjectid,
                               qahf.fstatus,
                               qahf.fobjmodification,
                               (select codereview.id
                                from codereview
                                where codereview.fobjectid = qahf.fobjectid
                                  and codereview.fslipno = qahf.fslipno) code_id,
                               (select codereview.id
                                from codereview
                                where codereview.fobjectid = 'Design Review'
                                  and codereview.fslipno = qahf.fslipno) design_id
                        from liaisonf,
                             qahf
                        where (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                          and qahf.fcreateusr in (select name from users where ammic_organization_id in {all_organization_tuple})
                          and qahf.fstatus = '3'
                          and qahf.ftesttyp = 'MCL'
                        union all
                        select distinct qahf.id,
                                        qahf.ftesttyp,
                                        qahf.fslipno,
                                        qahf.fslipno2 fslipno,
                                        qahf.fobjectid,
                                        qahf.fstatus,
                                        qahf.fnote,
                                        ''            code_id,
                                        ''            design_id
                        from qahf,
                             liaisonf
                        where qahf.ftesttyp = 'PCL'
                          and qahf.fstatus = '3'
                          and liaisonf.fodrno = qahf.fslipno
                          and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                                   (select name from users where ammic_organization_id in {all_organization_tuple}))
                      """

        confirm_dict = db_connection_execute(confirm_sql, 'dict')

        return Response(data=confirm_dict, status=status.HTTP_200_OK)


class MyRelease(APIView):

    def get(self, request):
        user = request.user

        all_organization_group_tuple = get_all_organization_group_belong_me(request)

        testing_sql = f"""
                       select *
                            from liaisonf
                            where fslipno in (
                                select fslipno
                                from (
                                     select qahf_c.fslipno, count(*) count
                                     from (
                                          select distinct fslipno, fstatus
                                          from qahf
                                          where fslipno in (
                                              select fslipno
                                              from liaisonf
                                              where fodrno in (
                                                  select fslipno
                                                  from qahf
                                                  where fslipno in (
                                                      select qahf_b.fslipno
                                                      from (select fslipno, count(*) count
                                                            from (select fslipno, fstatus from qahf where 
                                                            ftesttyp = 'PCL') qahf_a
                                                            group by fslipno) qahf_b
                                                      where qahf_b.count = 1)
                                                    and fstatus = '4')
                                                and liaisonf.fstatus = '3'
                                                and liaisonf.forganization in {all_organization_group_tuple})) qahf_c
                                     group by qahf_c.fslipno) a
                                where a.count = 1
                                union all
                                select fslipno
                                from (
                                     select a.fslipno, a.fstatus, count(*) count
                                     from (
                                          select distinct qahf.fslipno, qahf.fstatus
                                          from liaisonf,
                                               qahf
                                          where liaisonf.fslipno = qahf.fslipno
                                            and liaisonf.ftype <> '追加开发'
                                            and liaisonf.fstatus = '3'
                                            and liaisonf.forganization in {all_organization_group_tuple}) a
                                     group by a.fslipno, a.fstatus) b
                                where b.count = 1
                                  and b.fstatus = '4')
                            order by fslipno
                      """

        testing_dict = db_connection_execute(testing_sql, 'dict')

        return Response(data=testing_dict, status=status.HTTP_200_OK)

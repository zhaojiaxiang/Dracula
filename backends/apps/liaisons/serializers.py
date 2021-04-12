from datetime import date

from django.db import transaction
from rest_framework import serializers

from liaisons.models import Liaisons
from qa.models import QaHead
from rbac.models import Organizations
from utils.db_connection import man_power_connection_execute, db_connection_execute, query_single_with_no_parameter
from utils.slims import SLIMSExchange


class LiaisonsSerializer(serializers.ModelSerializer):
    fsystemcd = serializers.CharField(required=True, max_length=20, label='系统名称',
                                      error_messages={
                                          'required': '系统名称为必输项',
                                          'max_length': '系统名称最大长度为20'
                                      })
    fprojectcd = serializers.CharField(required=True, max_length=20, label='项目名称',
                                       error_messages={
                                           'required': '项目名称为必输项',
                                           'max_length': '项目名称最大长度为20'
                                       })
    fslipno = serializers.CharField(required=True, max_length=20, label='联络票号',
                                    error_messages={
                                        'required': '联络票号为必输项',
                                        'max_length': '联络票号最大长度为20'
                                    })
    fodrno = serializers.CharField(required=True, max_length=20, label='订单号',
                                   error_messages={
                                       'required': '订单号为必输项',
                                       'max_length': '订单号最大长度为20'
                                   })
    fstatus = serializers.CharField(read_only=True)
    fcreatedte = serializers.CharField(read_only=True)
    fcreateusr = serializers.CharField(read_only=True)
    forganization = serializers.IntegerField(read_only=True)
    fentdt = serializers.DateTimeField(read_only=True)
    fentusr = serializers.CharField(read_only=True)
    fupdtedt = serializers.DateTimeField(read_only=True)
    fupdteusr = serializers.CharField(read_only=True)
    fupdteprg = serializers.CharField(read_only=True)

    class Meta:
        model = Liaisons
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        try:
            new_slipno = validated_data['fslipno']
            new_sirno = validated_data['fsirno']
            fcreateusr = validated_data['fassignedto']
            fcreatedte = validated_data['fplnstart']

            is_exist = Liaisons.objects.filter(fslipno__exact=new_slipno)
            if is_exist.count() > 0:
                raise serializers.ValidationError("联络票已经存在")

            user = self.context['request'].user

            organization_id = user.ammic_organization.id
            if not user.ammic_organization.isgroup:
                organization_id = user.ammic_organization.parent.id

            liaison = Liaisons.objects.create(**validated_data)

            if new_sirno or len(new_sirno) > 0:
                liaison.fstatus = '2'
                liaison.fsirno = new_sirno
                liaison.fcreateusr = fcreateusr
                liaison.fcreatedte = fcreatedte
                liaison.factstart = fcreatedte
            else:
                liaison.fstatus = '1'
                liaison.fcreateusr = user.name
            liaison.forganization = organization_id
            liaison.fentusr = user.name
            liaison.fupdteprg = "Liaison No New"
            liaison.save()

            liaison_type = liaison.ftype
            liaison_order_no = liaison.fodrno
            if liaison_type == '追加开发':
                qahf = QaHead.objects.filter(fslipno__exact=liaison_order_no)
                if not qahf:
                    sql_str = f"select fnote from odrrlsf where fodrno = '{liaison_order_no}' "
                    note_list = man_power_connection_execute(sql_str)
                    fnote = note_list[0][0] if note_list else "******"

                    qahf = QaHead.objects.create()
                    qahf.ftesttyp = 'PCL'
                    qahf.fsystemcd = liaison.fsystemcd
                    qahf.fprojectcd = liaison.fprojectcd
                    qahf.fslipno = liaison_order_no
                    qahf.fobjectid = liaison_order_no + "(QA)"
                    qahf.fobjectnm = liaison_order_no + "(QA)"
                    qahf.fstatus = "1"
                    qahf.fnote = fnote if fnote else "******"
                    qahf.fentusr = user.name
                    qahf.fcreateusr = user.name
                    qahf.fupdteprg = "Liaison No New"
                    qahf.save()

            return liaison
        except Exception as ex:
            raise serializers.ValidationError(ex.args[0])

    @transaction.atomic()
    def update(self, instance, validated_data):
        try:
            if instance.fslipno != validated_data['fslipno']:
                is_exist = Liaisons.objects.filter(fslipno__exact=validated_data['fslipno'])
                if is_exist.count() > 0:
                    raise serializers.ValidationError("联络票已经存在")
            # 更新SLIMS
            slip_status = instance.fstatus
            if slip_status == "2" or slip_status == "3":
                sir_no = validated_data['fsirno']
                if sir_no or len(sir_no) > 0:
                    slims = SLIMSExchange(self.context['request'])
                    ret = slims.update_slims_overload(validated_data)

                    if ret < 1:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to fix MCL!")

            user = self.context['request'].user
            instance.fupdteusr = user.name
            instance.fupdteprg = "Liaison No Modify"
            instance.save()
        except Exception as ex:
            raise serializers.ValidationError(ex.args[0])
        return super().update(instance, validated_data)


class LiaisonUpdateStatusSerializer(serializers.ModelSerializer):
    fslipno = serializers.CharField(read_only=True)
    fodrno = serializers.CharField(read_only=True)

    class Meta:
        model = Liaisons
        fields = ("id", "fslipno", "fodrno", "fstatus")

    @transaction.atomic()
    def update(self, instance, validated_data):
        try:
            user = self.context['request'].user
            orig_status = instance.fstatus
            new_status = validated_data["fstatus"]
            sir_no = instance.fsirno
            slip_no = instance.fslipno
            current_date = date.today()
            status_diff = abs(int(orig_status) - int(new_status))
            slims = SLIMSExchange(self.context['request'])
            if status_diff > 1:
                raise serializers.ValidationError("联络票状态不可跨级修改！")
            if int(orig_status) < int(new_status):
                if new_status == "2":
                    new_sir_no = ""
                    if sir_no is None or len(sir_no) == 0:
                        # 联络开始时，生成Sir No，并更新到本系统中
                        new_sir_no = slims.insert_slims_overload(instance)

                        if new_sir_no is None or len(new_sir_no) == 0:
                            raise serializers.ValidationError(
                                "AMMIC2SLMS Service exception--Unable to generate Sir No!!")

                    instance.factstart = current_date
                    instance.fsirno = new_sir_no
                elif new_status == "3":
                    if sir_no is None:
                        raise serializers.ValidationError("无法结束该联络票--Sir No为空!")

                    qa_count_close = QaHead.objects.filter(fstatus__in=('3', '4'), fslipno__exact=slip_no).count()
                    qa_count = QaHead.objects.filter(fslipno__exact=slip_no).count()

                    if not (qa_count_close > 0 and qa_count_close == qa_count):
                        raise serializers.ValidationError("当前联络票不满足完成条件，QA没有结束")

                    # 联络票结束时，第一次更新MCL测试数据到SLIMS系统中
                    ret = slims.fix_slims_overload(sir_no, slip_no)

                    if ret < 0:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to fix MCL!")

                    instance.factend = current_date
                elif new_status == "4":
                    all_obj = QaHead.objects.filter(fslipno__exact=instance.fslipno)
                    confirmed_obj = QaHead.objects.filter(fslipno__exact=instance.fslipno, fstatus__exact="4")
                    if all_obj.count() != confirmed_obj.count():
                        raise serializers.ValidationError("该联络票下存在未确认的测试项")

                    pcl_objs = QaHead.objects.filter(fslipno__exact=instance.fodrno)
                    if pcl_objs:
                        for pcl in pcl_objs:
                            if pcl.fstatus != "4":
                                raise serializers.ValidationError("该联络票下的PCL没有确认")

                    if instance.freleaserpt is None or len(instance.freleaserpt.strip()) == 0:
                        raise serializers.ValidationError("请先上传变更报告书")

                    if sir_no is None or len(sir_no) == 0:
                        raise serializers.ValidationError("无法发布该联络票--Sir No为空!")

                    # 联络票发布时，第二次更新MCL测试数据到SLIMS系统中，先删除原始的MCL数据，在重新生成一遍
                    ret = slims.delete_mcl(sir_no, slip_no)

                    if ret < 0:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to delete MCL!")

                    ret = slims.fix_slims_overload(sir_no, slip_no)

                    if ret < 0:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to fix MCL!")

                    ret = slims.close_slims(sir_no)
                    if ret < 0:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to close Sir No!")

                    instance.freleasedt = current_date
            else:
                if new_status == "3":
                    instance.freleasedt = None
                elif new_status == "2":
                    is_exist = QaHead.objects.filter(fslipno__exact=instance.fslipno, fstatus__exact="4")
                    if is_exist.count() > 0:
                        raise serializers.ValidationError("该联络票下存在已确认的测试对象，不可回滚到开始状态")

                    # 状态回滚到进行中时，删除SLIMS系统中的MCL数据
                    ret = slims.delete_mcl(sir_no, slip_no)

                    if ret < 0:
                        raise serializers.ValidationError("AMMIC2SLMS Service exception--Unable to delete MCL!")

                    instance.factend = None
                    instance.factmanpower = 0
                elif new_status == "1":
                    is_exist = QaHead.objects.filter(fslipno__exact=instance.fslipno)
                    if is_exist.count() > 0:
                        raise serializers.ValidationError("已经录入测试对象，不可回滚到初始状态")

                    # 状态回滚到初始时，将SLIMS中的Sir No失效
                    ret = slims.delete_slims(sir_no)
                    if ret < 1:
                        raise serializers.ValidationError(
                            "AMMIC2SLMS Service exception--Unable to fail Sir No!")
                    instance.factstart = None
                    instance.fsirno = None

            instance.fupdteusr = user.name
            instance.fupdteprg = "Liaison No Modify"
            instance.save()
            return super().update(instance, validated_data)
        except Exception as ex:
            raise serializers.ValidationError(ex.args[0])


class QaProjectSerializer(serializers.ModelSerializer):
    orderno = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    partner = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    slipno_all = serializers.SerializerMethodField()
    slipno_working = serializers.SerializerMethodField()
    slipno_close = serializers.SerializerMethodField()
    slipno_release = serializers.SerializerMethodField()
    objectcount = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Liaisons
        fields = (
            'orderno', 'note', 'partner', 'project', 'slipno_all', 'slipno_working', 'slipno_close', 'slipno_release',
            'objectcount', 'status', 'organization')

    def get_orderno(self, obj):
        return obj['fodrno']

    def get_note(self, obj):
        sql_str = f"select fnote from odrrlsf where fodrno = '{obj['fodrno']}' "
        note_list = man_power_connection_execute(sql_str)
        return note_list[0][0] if note_list else "******"

    def get_project(self, obj):
        project = Liaisons.objects.filter(fodrno__exact=obj['fodrno']).values('fprojectcd').distinct()
        return project[0]['fprojectcd']

    def get_partner(self, obj):
        order_partner_sql = f"select fassignedto, fleader, fhelper from liaisonf where fodrno = '{obj['fodrno']}'"
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
        return len(user_list)

    def get_slipno_all(self, obj):
        liaison = Liaisons.objects.filter(fodrno__exact=obj['fodrno'])
        if liaison:
            return liaison.count()
        return 0

    def get_slipno_working(self, obj):
        liaison = Liaisons.objects.filter(fodrno__exact=obj['fodrno'], fstatus__exact=2)
        if liaison:
            return liaison.count()
        return 0

    def get_slipno_close(self, obj):
        liaison = Liaisons.objects.filter(fodrno__exact=obj['fodrno'], fstatus__exact=3)
        if liaison:
            return liaison.count()
        return 0

    def get_slipno_release(self, obj):
        liaison = Liaisons.objects.filter(fodrno__exact=obj['fodrno'], fstatus__exact=4)
        if liaison:
            return liaison.count()
        return 0

    def get_objectcount(self, obj):
        test_object_sql = f"select count(*) from qahf where fslipno in (select fslipno from liaisonf " \
                          f"where fodrno = '{obj['fodrno']}')"
        test_object_list = query_single_with_no_parameter(test_object_sql, "list")
        test_object = test_object_list[0]
        return test_object

    def get_status(self, obj):
        order_slipno_working = self.get_slipno_working(obj)
        order_slipno_close = self.get_slipno_close(obj)
        order_slipno_all = self.get_slipno_all(obj)
        order_slipno_release = self.get_slipno_release(obj)

        order_status = 1
        if order_slipno_working > 0 or \
                (order_slipno_working == 0 and order_slipno_close > 0 and order_slipno_close != order_slipno_all):
            order_status = 2
        elif order_slipno_working == 0 and order_slipno_close == order_slipno_all:
            order_status = 3
        elif order_slipno_release == order_slipno_all:
            order_status = 4

        return order_status

    def get_organization(self, obj):
        organizations = Organizations.objects.values('name').filter(pk=obj['forganization'])
        return organizations[0]['name']

from datetime import date

from django.db import transaction
from rest_framework import serializers

from liaisons.models import Liaisons
from qa.models import QaHead
from utils.db_connection import man_power_connection_execute


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
    fentdt = serializers.DateField(read_only=True)
    fentusr = serializers.CharField(read_only=True)
    fupdtedt = serializers.DateField(read_only=True)
    fupdteusr = serializers.CharField(read_only=True)
    fupdteprg = serializers.DateField(read_only=True)

    class Meta:
        model = Liaisons
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):

        new_slipno = validated_data['fslipno']

        is_exist = Liaisons.objects.filter(fslipno__exact=new_slipno)
        if is_exist.count() > 0:
            raise serializers.ValidationError("联络票已经存在")

        user = self.context['request'].user
        liaison = Liaisons.objects.create(**validated_data)
        liaison.fstatus = '1'
        liaison.fcreateusr = user.name
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

    @transaction.atomic()
    def update(self, instance, validated_data):

        if instance.fslipno != validated_data['fslipno']:
            is_exist = Liaisons.objects.filter(fslipno__exact=validated_data['fslipno'])
            if is_exist.count() > 0:
                raise serializers.ValidationError("联络票已经存在")

        user = self.context['request'].user
        instance.fupdteusr = user.name
        instance.fupdteprg = "Liaison No Modify"
        instance.save()
        return super().update(instance, validated_data)


class LiaisonUpdateStatusSerializer(serializers.ModelSerializer):

    fslipno = serializers.CharField(read_only=True)
    fodrno = serializers.CharField(read_only=True)

    class Meta:
        model = Liaisons
        fields = ("id", "fslipno", "fodrno", "fstatus")

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        orig_status = instance.fstatus
        new_status = validated_data["fstatus"]
        current_date = date.today()
        status_diff = abs(int(orig_status) - int(new_status))
        if status_diff > 1:
            raise serializers.ValidationError("联络票状态不可跨级修改！")
        if int(orig_status) < int(new_status):
            if new_status == "2":
                instance.factstart = current_date
            elif new_status == "3":
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
                instance.freleasedt = current_date
        else:
            if new_status == "3":
                instance.freleasedt = None
            elif new_status == "2":
                is_exist = QaHead.objects.filter(fslipno__exact=instance.fslipno, fstatus__exact="4")
                if is_exist.count() > 0:
                    raise serializers.ValidationError("该联络票下存在已确认的测试对象，不可回滚到开始状态")
                instance.factend = None
                instance.factmanpower = 0
            elif new_status == "1":
                is_exist = QaHead.objects.filter(fslipno__exact=instance.fslipno)
                if is_exist.count() > 0:
                    raise serializers.ValidationError("已经录入测试对象，不可回滚到初始状态")
                instance.factstart = None

        instance.fupdteusr = user.name
        instance.fupdteprg = "Liaison No Modify"
        instance.save()
        return super().update(instance, validated_data)

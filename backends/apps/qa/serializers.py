import datetime

from django.db import transaction
from django.db.models import Max
from math import ceil
from rest_framework import serializers

from liaisons.models import Liaisons
from qa.models import QaHead, QaDetail
from reviews.models import CodeReview


class MCLQaHeadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    fcreatedte = serializers.DateTimeField(read_only=True)
    fcreateusr = serializers.CharField(read_only=True)
    fslipno2 = serializers.IntegerField(read_only=True)
    # ftesttyp = serializers.CharField(read_only=True)

    qadfcount = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = ('id', 'fsystemcd', 'fprojectcd', 'fslipno', 'fslipno2', 'fobjectid', 'fobjmodification',
                  'fcreatedte', 'fcreateusr', 'fstatus', 'ftesttyp', 'qadfcount', 'freviewcode', 'flevel')

    def get_qadfcount(self, obj):
        qadf = QaDetail.objects.filter(qahf_id__exact=obj.id)
        return qadf.count()

    @transaction.atomic()
    def create(self, validated_data):

        test_type = validated_data['ftesttyp']
        slip_no2 = 1
        if test_type == 'MCL':
            is_exist = QaHead.objects.filter(fslipno__exact=validated_data['fslipno'],
                                             fobjectid__exact=validated_data['fobjectid'])

            if is_exist.count() > 0:
                raise serializers.ValidationError("该测试对象已经在该联络下存在")
        else:
            slip_no2 = QaHead.objects.aggregate(Max('fslipno')) + 1

        user = self.context['request'].user
        qahead = QaHead.objects.create(**validated_data)
        qahead.ftesttyp = 'MCL'
        qahead.fobjectnm = validated_data['fobjectid']
        qahead.fcreateusr = user.name
        qahead.fslipno2 = slip_no2
        qahead.fstatus = '1'
        qahead.fentusr = user.name
        qahead.fupdteprg = 'QA New'
        qahead.save()
        return qahead

    @transaction.atomic()
    def update(self, instance, validated_data):
        qa_details = QaDetail.objects.filter(qahf__exact=instance)
        orig_status = instance.fstatus
        new_status = validated_data['fstatus']
        user = self.context['request'].user

        diff_status = int(new_status) - int(orig_status)
        if abs(diff_status) > 1:
            raise serializers.ValidationError("测试对象状态不可跨级修改，系统流程控制Bug！")

        if diff_status > 0:
            if new_status == '2':
                """审核"""
                lot = instance.flastapprovallot + 1
                instance.fstatus = new_status
                instance.fauditdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flastapprovallot = lot
                instance.fauditor = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval"
                instance.save()

                for qa in qa_details:
                    if qa.fapproval != "Y":
                        qa.fapproval = "Y"
                        qa.fapprovallot = lot
                        qa.fupdteusr = user.name
                        qa.fupdteprg = "QA Approval"
                        qa.save()

            if new_status == '3':
                """测试结果提交"""
                if instance.ftesttyp == "MCL":
                    if instance.fobjmodification is None:
                        raise serializers.ValidationError("请先填写测试对象修改概要")

                    if instance.fcomplexity is None:
                        raise serializers.ValidationError("请先填写测试明细")

                    if instance.fttlcodelines is None:
                        raise serializers.ValidationError("请先填写修改明细")

                    code_review = CodeReview.objects.filter(fobjectid__exact=instance.fobjectid,
                                                            fslipno__exact=instance.fslipno)
                    if code_review.count() == 0:
                        raise serializers.ValidationError("请先填写代码Review")

                    liaison = Liaisons.objects.filter(fslipno__exact=instance.fslipno)
                    if liaison[0].ftype == "追加开发":
                        design_review = CodeReview.objects.filter(fobjectid__exact="Design Review",
                                                                  fslipno__exact=instance.fslipno)
                        if design_review.count() == 0:
                            raise serializers.ValidationError("请先填写设计Review")

                instance.fstatus = new_status
                instance.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.ftestusr = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Submit"
                instance.save()

            if new_status == '4':
                """确认"""
                instance.fstatus = new_status
                instance.fconfirmdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flevel = validated_data['flevel']
                instance.freviewcode = validated_data['freviewcode']
                instance.fconfirmusr = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Confirm"
                instance.save()
        elif diff_status < 0:
            if new_status == '3':
                """取消确认"""
                instance.fstatus = new_status
                instance.fconfirmdte = None
                instance.fconfirmusr = ""
                instance.flevel = ''
                instance.freviewcode = ''
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Confirm Cancel"
                instance.save()

            if new_status == '2':
                """取消结果提交"""
                instance.fstatus = new_status
                instance.ftestdte = None
                instance.ftestusr = ""
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Submit Cancel"
                instance.save()

            if new_status == '1':
                """审核审核， 该逻辑原则上不会出现"""
                lot = instance.flastapprovallot - 1
                instance.fstatus = new_status
                instance.fauditdte = None
                instance.fauditor = ""
                instance.flastapprovallot = lot
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval Cancel"
                instance.save()

                for qa in qa_details:
                    qa.fapproval = "N"
                    qa.fupdteusr = user.name
                    qa.fapprovallot = qa.fapprovallot - 1
                    qa.fupdteprg = "QA Approval Cancel"
                    qa.save()
        else:
            if new_status == '2':
                """审核"""
                lot = instance.flastapprovallot + 1
                instance.fstatus = new_status
                instance.fauditdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flastapprovallot = lot
                instance.fauditor = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval"
                instance.save()

                for qa in qa_details:
                    if qa.fapproval != "Y":
                        qa.fapproval = "Y"
                        qa.fapprovallot = lot
                        qa.fupdteusr = user.name
                        qa.fupdteprg = "QA Approval"
                        qa.save()

        return instance


class QaHeadDisplayNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaHead
        fields = ('fnote',)


class QaHeadUpdateObjectSummarySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = QaHead
        fields = ('id', 'fobjmodification')


class QaHeadModifyDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = QaHead
        fields = ('id', 'fttlcodelines', 'fmodifiedlines', 'fcomplexity')


class QaHeadTargetAndActualSerializer(serializers.ModelSerializer):
    target_tests = serializers.SerializerMethodField()
    target_regressions = serializers.SerializerMethodField()
    target_total = serializers.SerializerMethodField()
    target_ng = serializers.SerializerMethodField()
    actual_tests = serializers.SerializerMethodField()
    actual_regressions = serializers.SerializerMethodField()
    actual_total = serializers.SerializerMethodField()
    actual_ng = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = (
        'id', 'fttlcodelines', 'fmodifiedlines', 'fcomplexity', 'fstatus', 'target_tests', 'target_regressions',
        'target_total', 'target_ng', 'actual_tests', 'actual_regressions', 'actual_total', 'actual_ng')

    def get_target_tests(self, obj):
        if obj.fmodifiedlines:
            return ceil(obj.fmodifiedlines * obj.fcomplexity / 11)
        return 0

    def get_target_regressions(self, obj):
        if obj.fttlcodelines:
            return ceil(obj.fttlcodelines / 50)
        return 0

    def get_target_total(self, obj):
        if obj.fttlcodelines:
            return self.get_target_regressions(obj) + self.get_target_tests(obj)
        return 0

    def get_target_ng(self, obj):
        if obj.fmodifiedlines:
            return ceil(self.get_target_tests(obj) / 11)
        return 0

    def get_actual_tests(self, obj):
        return QaDetail.objects.filter(fregression__exact='N',
                                       fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_regressions(self, obj):
        return QaDetail.objects.filter(fregression__exact='Y',
                                       fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_total(self, obj):
        return QaDetail.objects.filter(fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_ng(self, obj):
        return QaDetail.objects.filter(fresult__contains='NG',
                                       qahf_id__exact=obj.id).count()


class QaDetailSerializer(serializers.ModelSerializer):
    # qahf = QaHeadSerializer()  # 获取反向获取外键的相关字段

    id = serializers.IntegerField(read_only=True)
    fimpdte = serializers.DateField(read_only=True)
    fimpusr = serializers.DateField(read_only=True)
    ftestdte = serializers.DateField(read_only=True)
    ftestusr = serializers.CharField(read_only=True)
    fapproval = serializers.CharField(read_only=True)
    fngcnt = serializers.IntegerField(read_only=True)
    fresult = serializers.CharField(read_only=True)
    fcontent_text = serializers.CharField(read_only=True)

    class Meta:
        model = QaDetail
        fields = ('id', 'fclass1', 'fregression', 'fcontent', 'fsortrule', 'fimpdte', 'fimpusr', 'ftestdte', 'ftestusr',
                  'fapproval', 'fresult', 'fngcnt', 'qahf', 'fapproval', 'fcontent_text')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=QaDetail.objects.all(),
        #         fields=['fcontent', 'qahf'],
        #         message="该测试项已经在该对象下存在"
        #     )
        # ]

    @transaction.atomic()
    def create(self, validated_data):
        is_exist = QaDetail.objects.filter(fcontent__exact=validated_data['fcontent'],
                                           qahf_id__exact=validated_data['qahf'])
        if is_exist.count() > 0:
            raise serializers.ValidationError("该测试项已经在该对象下存在")

        user = self.context['request'].user
        qadetail = QaDetail.objects.create(**validated_data)
        qadetail.fimpusr = user.name
        qadetail.fentusr = user.name
        qadetail.fupdteprg = "QA New"
        qadetail.save()
        return qadetail

    @transaction.atomic()
    def update(self, instance, validated_data):
        approval = instance.fapproval
        result = instance.fresult

        if approval == "Y":
            raise serializers.ValidationError('已经审核的测试项不可修改')
        else:
            if result:
                raise serializers.ValidationError('存在测试结果的测试项不可修改')
        return super().update(instance, validated_data)


class QaDetailUpdateResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = QaDetail
        fields = ('id', 'fresult')

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        result_original = instance.fresult
        result_present = validated_data['fresult']

        if result_original:
            if "NG" in result_original and result_present == "OK":
                raise serializers.ValidationError("测试结果不可由NG修改为OK！！！")

            if result_original == "CANCEL":
                raise serializers.ValidationError("已经取消的测试项不可修改")

        instance.fresult = result_present
        instance.ftestusr = user.name
        instance.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
        instance.save()
        return instance


class QaDetailUpdateContentTextSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = QaDetail
        fields = ('id', 'status', 'fcontent', 'fcontent_text')

    def get_status(self, obj):
        return obj.qahf.fstatus

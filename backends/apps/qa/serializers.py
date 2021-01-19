import datetime

from django.db import transaction
from rest_framework import serializers

from qa.models import QaHead, QaDetail


class QaHeadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    fcreatedte = serializers.DateTimeField(read_only=True)
    fcreateusr = serializers.CharField(read_only=True)
    fstatus = serializers.CharField(read_only=True)
    ftesttyp = serializers.CharField(read_only=True)

    qadfcount = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = ('id', 'fsystemcd', 'fprojectcd', 'fslipno', 'fobjectid', 'fobjmodification',
                  'fcreatedte', 'fcreateusr', 'fstatus', 'ftesttyp', 'qadfcount')

    def get_qadfcount(self, obj):
        qadf = QaDetail.objects.filter(qahf_id__exact=obj.id)
        return qadf.count()

    @transaction.atomic()
    def create(self, validated_data):

        is_exist = QaHead.objects.filter(fslipno__exact=validated_data['fslipno'],
                                         fobjectid__exact=validated_data['fobjectid'])

        if is_exist.count() > 0:
            raise serializers.ValidationError("该测试对象已经在该联络下存在")

        user = self.context['request'].user
        qahead = QaHead.objects.create(**validated_data)
        qahead.ftesttyp = 'MCL'
        qahead.fobjectnm = validated_data['fobjectid']
        qahead.fcreateusr = user.name
        qahead.fstatus = '1'
        qahead.fentusr = user.name
        qahead.fupdteprg = 'MCL QA New'
        qahead.save()
        return qahead

    @transaction.atomic()
    def update(self, instance, validated_data):
        qa_detail = QaDetail.objects.filter(qahf__exact=instance)
        if instance.fstatus != '1':
            raise serializers.ValidationError('只有在初始状态下可以修改')
        elif qa_detail:
            raise serializers.ValidationError('已经存在测试项不可修改')
        else:
            user = self.context['request'].user
            instance.fobjectid = validated_data['fobjectid']
            instance.fobjectnm = validated_data['fobjectid']
            instance.fupdteusr = user.name
            instance.fupdteprg = "MCL QA Modify"
            instance.save()
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

    class Meta:
        model = QaDetail
        fields = ('id', 'fcontent_text')


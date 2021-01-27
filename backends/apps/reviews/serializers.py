from rest_framework import serializers

from reviews.models import CodeReview


class DesignReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CodeReview
        fields = ('id', 'fslipno', 'fobjectid', 'fcontent_text')


class CodeReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CodeReview
        fields = ('id', 'fslipno', 'fobjectid', 'fcontent_text')

from rest_framework import serializers

from systems.models import Systems


class SystemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Systems
        fields = "__all__"

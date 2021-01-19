
from rest_framework import serializers

from liaisons.models import Liaisons
from qa.models import QaHead
from qa.serializers import QaHeadDisplayNoteSerializer


class ReportLiaisonSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField()

    class Meta:
        model = Liaisons
        fields = ('fsystemcd', 'fprojectcd', 'fodrno', 'note')

    def get_note(self, obj):
        all_qahf = QaHead.objects.filter(fslipno__exact=obj['fodrno'])
        qahf_serializer = QaHeadDisplayNoteSerializer(all_qahf, many=True, context={'request': self.context['request']})
        return qahf_serializer.data[0]['fnote'] if qahf_serializer.data else '******'

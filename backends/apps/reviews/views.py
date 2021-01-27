from django.db.models import Q
from rest_framework import mixins, viewsets

from reviews.models import CodeReview
from reviews.serializers import DesignReviewSerializer, CodeReviewSerializer


class DesignReviewViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):

    def get_queryset(self):
        return CodeReview.objects.filter(fobjectid__exact="Design Review")

    serializer_class = DesignReviewSerializer


class CodeReviewViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    def get_queryset(self):
        return CodeReview.objects.filter(~Q(CodeReview.fobjectid != "Design Review"))

    serializer_class = CodeReviewSerializer

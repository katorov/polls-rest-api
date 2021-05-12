from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from polls import models
from polls.api import serializers
from polls.api.mixins import MultiSerializerViewSetMixin
from polls.api.permissions import ReadOnly


class PollViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Представление для работы с опросами"""
    queryset = models.Poll.objects.all()
    serializer_class = serializers.PollSerializer
    serializer_action_classes = {
        'create': serializers.PollCreateSerializer
    }
    permission_classes = [IsAdminUser | ReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_admin = bool(self.request.user and self.request.user.is_staff)
        if not is_admin:
            return queryset.available()
        return queryset


class QuestionViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Представление для работы с вопросами в опросах"""
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    serializer_action_classes = {
        'create': serializers.QuestionCreateSerializer
    }
    permission_classes = [IsAdminUser]

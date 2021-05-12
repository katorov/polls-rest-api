from rest_framework.viewsets import ModelViewSet

from polls import models
from polls.api import serializers
from polls.api.mixins import MultiSerializerViewSetMixin


class PollViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Представление для работы с опросами"""
    queryset = models.Poll.objects.available()
    serializer_class = serializers.PollSerializer
    serializer_action_classes = {
        'create': serializers.PollCreateSerializer
    }


class QuestionViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Представление для работы с вопросами в опросах"""
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    serializer_action_classes = {
        'create': serializers.QuestionCreateSerializer
    }

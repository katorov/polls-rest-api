from rest_framework import serializers

from polls import models


class PollSerializer(serializers.ModelSerializer):
    """Serializer для просмотра/изменения/удаления опросов"""
    class Meta:
        model = models.Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']
        read_only_fields = ['start_date']


class PollCreateSerializer(serializers.ModelSerializer):
    """Serializer для добавления опросов"""
    class Meta:
        model = models.Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer для просмотра/изменения/удаления вопросов"""
    poll_name = serializers.ReadOnlyField(source='poll.name')

    class Meta:
        model = models.Question
        fields = ['id', 'question_text', 'question_type', 'poll', 'poll_name']
        read_only_fields = ['poll', 'poll_name']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer для создания вопросов"""
    poll_name = serializers.ReadOnlyField(source='poll.name')

    class Meta:
        model = models.Question
        fields = ['id', 'question_text', 'question_type', 'poll', 'poll_name']
        read_only_fields = ['poll_name']

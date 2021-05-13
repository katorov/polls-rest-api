from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polls import models
from polls.models import Question
from polls.services import create_question_choices, update_question_choices, \
    create_completed_poll


class CustomerAnswerSerializer(serializers.ModelSerializer):
    """Serializer для ответов на пройденные опросы"""
    question_text = serializers.ReadOnlyField(source='question.question_text')

    def validate(self, data):
        question = data.get('question')
        question_type = question.question_type
        answer_choice = data.get('answer_choice')
        answer_text = data.get('answer_text')

        if question_type == Question.SIMPLE and not answer_text:
            raise ValidationError(f'Текст ответа обязателен для данного вопроса')

        if question_type == Question.CHECKBOXES and not answer_choice:
            raise ValidationError(f'Вариант ответа обязателен для данного вопроса')

        if question_type == Question.MULTIPLE_CHOICE and not answer_choice:
            raise ValidationError(f'Вариант ответа обязателен для данного вопроса')

        return super().validate(data)

    class Meta:
        model = models.CustomerAnswer
        fields = ['id', 'question', 'question_text', 'answer_choice', 'answer_text']
        read_only_fields = ['id', 'question_text']


class CustomerSerializer(serializers.Serializer):
    """Serializer для пользователей, прошедших опрос"""
    customer_id = serializers.IntegerField()

    def validate_customer_id(self, value):
        if value <= 0:
            raise ValidationError('Поле customer_id не может быть меньше или равно 0')
        return value


class CompletedPollSerializer(serializers.ModelSerializer):
    """Serializer для пройденных опросов и ответов"""
    answers = CustomerAnswerSerializer(many=True, required=True, allow_null=False)
    customer = CustomerSerializer()

    class Meta:
        model = models.CompletedPoll
        fields = ['id', 'customer', 'poll', 'answers']
        read_only_fields = ['id']

    def validate(self, data):
        poll = data.get('poll')
        answers_data = data.get('answers')
        for answer_data in answers_data:
            question = answer_data['question']
            if question.poll != poll:
                raise ValidationError(f'Вопрос {question.id} не принадлежит данному опросу')
        return super().validate(data)

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        answers_data = validated_data.pop('answers')
        poll = validated_data.pop('poll')
        with transaction.atomic():
            completed_poll = create_completed_poll(customer['customer_id'], poll, answers_data)
        return completed_poll


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """Serializer для вариантов ответа на вопросы"""
    id = serializers.IntegerField(required=False)
    question_text = serializers.ReadOnlyField(source='question.question_text')

    class Meta:
        model = models.QuestionChoice
        fields = ['id', 'choice_text', 'question', 'question_text']
        read_only_fields = ['question', 'question_text']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer для просмотра/изменения/удаления вопросов"""
    poll_name = serializers.ReadOnlyField(source='poll.name')
    choices = QuestionChoiceSerializer(many=True, required=False)
    question_type = serializers.ChoiceField(choices=Question.QUESTION_TYPES)

    class Meta:
        model = models.Question
        fields = ['id', 'question_text', 'question_type', 'poll', 'poll_name', 'choices']
        read_only_fields = ['id', 'poll', 'poll_name']

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', list())
        with transaction.atomic():
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            update_question_choices(instance, choices_data)
        return instance


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer для создания вопросов"""
    poll_name = serializers.ReadOnlyField(source='poll.name')
    choices = QuestionChoiceSerializer(many=True, required=False)
    question_type = serializers.ChoiceField(choices=Question.QUESTION_TYPES)

    class Meta:
        model = models.Question
        fields = ['id', 'question_text', 'question_type', 'poll', 'poll_name', 'choices']
        read_only_fields = ['id', 'poll_name']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        question = models.Question(**validated_data)
        with transaction.atomic():
            question.save()
            create_question_choices(question, choices_data)
        return question


class PollSerializer(serializers.ModelSerializer):
    """Serializer для просмотра/изменения/удаления опросов"""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'questions']
        read_only_fields = ['start_date', 'questions']


class PollCreateSerializer(serializers.ModelSerializer):
    """Serializer для добавления опросов"""

    class Meta:
        model = models.Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']
        read_only_fields = ['id']

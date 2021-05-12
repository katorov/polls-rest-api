import datetime

from django.db import models


class TimestampModel(models.Model):
    """Абстрактная модель с полями даты создания и даты изменения"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['created_at']


class PollQuerySet(models.QuerySet):
    """Базовый QuerySet опроса"""

    def available(self):
        """Получить активные опросы"""
        today = datetime.date.today()
        return self.filter(start_date__lte=today, end_date__gte=today)


class Poll(TimestampModel):
    """Опрос"""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата старта', db_index=True)
    end_date = models.DateField('Дата окончания', db_index=True)

    objects = PollQuerySet.as_manager()

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['start_date']

    def __str__(self):
        return self.name


class Question(TimestampModel):
    """Вопрос в опросе"""
    SIMPLE, MULTIPLE_CHOICE, CHECKBOXES = 'т', 'ов', 'мв'
    QUESTION_TYPES = (
        (SIMPLE, 'Ответ текстом'),
        (MULTIPLE_CHOICE, 'Ответ с выбором одного варианта'),
        (CHECKBOXES, 'Ответ с выбором нескольких вариантов'),
    )

    question_text = models.TextField('Текст вопроса')
    question_type = models.CharField('Тип вопроса', max_length=2, choices=QUESTION_TYPES,
                                     db_index=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Опрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.question_type}] {self.question_text}'


class Customer(TimestampModel):
    """Пользователь, прошедший опрос"""
    customer_id = models.PositiveBigIntegerField('id', primary_key=True)

    class Meta:
        verbose_name = 'Пользователь, прошедший опрос'
        verbose_name_plural = 'Пользователи, прошедшие опросы'

    def __str__(self):
        return f'{self.customer_id}'


class CompletedPoll(TimestampModel):
    """Пройденный опрос"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Опрос')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Пройденный опрос'
        verbose_name_plural = 'Пройденные опросы'
        ordering = ['customer', 'created_at']

    def __str__(self):
        return f'{self.poll.name}'


class QuestionChoice(TimestampModel):
    """Вариант ответа на вопрос"""
    choice_text = models.CharField('Вариант ответа', max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['question', 'created_at']

    def __str__(self):
        return f'{self.choice_text}'


class CustomerAnswer(TimestampModel):
    """Ответ пользователя на вопрос"""
    answer_choice = models.ForeignKey(
        QuestionChoice, on_delete=models.CASCADE,
        verbose_name='Выбранный вариант ответа',
        null=True, blank=True
    )
    answer_text = models.CharField('Ответ', max_length=255, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    poll = models.ForeignKey(CompletedPoll, on_delete=models.CASCADE, verbose_name='Опрос')

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'
        ordering = ['poll', 'question', 'created_at']

    def __str__(self):
        return self.answer_text if self.answer_text else self.answer_choice.choice_text

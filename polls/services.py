from polls.models import QuestionChoice, Customer, CustomerAnswer, CompletedPoll


def create_question_choices(question: QuestionChoice, choices_data: list) -> None:
    """Добавить варианты ответов на вопрос"""
    choices = [QuestionChoice(question=question, **choice_data) for choice_data in choices_data]
    QuestionChoice.objects.bulk_create(choices)


def update_question_choices(question: QuestionChoice, choices_data: list) -> None:
    """Обновить варианты ответов на вопрос"""
    # Удалить все, если передан пустой список
    if not choices_data:
        question.choices.all().delete()

    current_choices = {choice.id: choice for choice in question.choices.all()}
    data_choices_with_id = {}
    data_choices_without_id = []

    for choice in choices_data:
        choice_id = choice.get('id', None)
        if choice_id and QuestionChoice.objects.filter(id=choice['id']).exists():
            data_choices_with_id[choice_id] = choice
        elif not choice_id:
            data_choices_without_id.append(choice)

    # Удалить существующие записи, если их нет в переданных данных
    to_delete_records_ids = set(current_choices.keys()) - set(data_choices_with_id.keys())
    QuestionChoice.objects.filter(id__in=to_delete_records_ids).delete()

    # Изменить существующие записи, если они есть в переданных данных
    for choice_id, choice_data in data_choices_with_id.items():
        choice_data.pop('id', None)
        QuestionChoice.objects.filter(id=choice_id).update(**choice_data)

    # Добавить новые записи
    create_question_choices(question, data_choices_without_id)


def create_customer_answers(completed_poll, answers_data: list) -> None:
    answers = [CustomerAnswer(poll=completed_poll, **answer_data) for answer_data in answers_data]
    CustomerAnswer.objects.bulk_create(answers)


def create_completed_poll(customer_id: int, poll, answers_data: list) -> CompletedPoll:
    customer, _ = Customer.objects.get_or_create(customer_id=customer_id)
    completed_poll = CompletedPoll.objects.create(poll=poll, customer=customer)
    create_customer_answers(completed_poll, answers_data)
    return completed_poll

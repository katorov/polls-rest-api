from django.contrib import admin

from polls import models


class QuestionInline(admin.TabularInline):
    model = models.Question


class QuestionChoiceInline(admin.TabularInline):
    model = models.QuestionChoice


class CustomerAnswerInline(admin.TabularInline):
    model = models.CustomerAnswer


@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'created_at')
    inlines = [QuestionInline]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'question_text', 'question_type', 'created_at')
    inlines = [QuestionChoiceInline]
    list_filter = ('poll',)


@admin.register(models.CompletedPoll)
class CompletedPollAdmin(admin.ModelAdmin):
    list_display = ('customer', 'poll', 'created_at')
    inlines = [CustomerAnswerInline]


@admin.register(models.QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'created_at')
    list_filter = ('question',)


@admin.register(models.CustomerAnswer)
class CustomerAnswerAdmin(admin.ModelAdmin):
    list_display = ('poll', 'question', 'answer_choice', 'answer_text', 'created_at')
    list_filter = ('poll', 'question')

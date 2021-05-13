from django.urls import path, include
from rest_framework.routers import DefaultRouter

from polls.api import views

router = DefaultRouter()
router.register(r'polls', views.PollViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'completed_polls', views.CompletedPollViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

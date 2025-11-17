from django.urls import path
from .views import ChatbotAPIView, ChatHistoryAPIView

urlpatterns = [
    path("ask/", ChatbotAPIView.as_view(), name="chatbot-ask"),
    path("history/", ChatHistoryAPIView.as_view(), name="chatbot-history"),
]

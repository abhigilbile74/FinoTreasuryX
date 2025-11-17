from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import get_user_model

from .serializers import ChatMessageSerializer
from .models import ChatMessage
from .ml.intent_classifier import classify_intent
from .services.openai_service import gpt_reply
from .services.transaction_analysis import analyze_transactions_for_user
from .services.budget_advisor import suggest_budget_changes
from .services.portfolio_advisor import portfolio_advice

User = get_user_model()

class ChatbotAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        text = request.data.get("message", "")
        if not text or not text.strip():
            return Response({"error": "message required"}, status=status.HTTP_400_BAD_REQUEST)

        text = text.strip()

        # classify intent (keyword / ML hybrid)
        intent = classify_intent(text)

        # route to handlers
        if intent == "transactions_summary":
            reply = analyze_transactions_for_user(user)
        elif intent == "budget_advice":
            reply = suggest_budget_changes(user)
        elif intent == "investment":
            reply = portfolio_advice(user, text)
        else:
            # Compose a short system prompt context + user message
            prompt = f"You are a concise personal finance assistant. User asked: {text}"
            reply = gpt_reply(prompt, user_id=getattr(user, "id", None))

        # save chat
        chat = ChatMessage.objects.create(user=user, user_message=text, bot_reply=reply, intent=intent)
        serializer = ChatMessageSerializer(chat)
        # Return response with both 'reply' and 'bot_reply' for compatibility
        response_data = serializer.data
        response_data['reply'] = reply  # Add 'reply' field for frontend compatibility
        return Response(response_data, status=status.HTTP_201_CREATED)


class ChatHistoryAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        # return last 200 messages
        return ChatMessage.objects.filter(user=user).order_by("-created_at")[:200]

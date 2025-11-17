from django.test import TestCase
from django.contrib.auth import get_user_model
from .ml.intent_classifier import classify_intent

User = get_user_model()

class ChatbotSmokeTests(TestCase):
    def test_intents(self):
        self.assertEqual(classify_intent("How much did I spend last month?"), "transactions_summary")
        self.assertEqual(classify_intent("Help me save money"), "budget_advice")
        self.assertEqual(classify_intent("Where should I invest?"), "investment")
        self.assertEqual(classify_intent("Hi there!"), "greeting")

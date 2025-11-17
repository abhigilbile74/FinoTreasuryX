# backend/transactions/serializers.py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'type', 'amount', 'description', 'category', 'date', 'budget']
        read_only_fields = ['id', 'user']

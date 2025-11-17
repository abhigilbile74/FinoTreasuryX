from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'amount', 'spent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'spent', 'created_at', 'updated_at']

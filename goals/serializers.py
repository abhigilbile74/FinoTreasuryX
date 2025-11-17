from rest_framework import serializers
from .models import Goal, Contribution, StrategyItem
from decimal import Decimal

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['id', 'goal', 'amount', 'date', 'note', 'created_at']
        read_only_fields = ['id', 'created_at']

class StrategyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyItem
        fields = ['id', 'goal', 'method', 'monthly_contribution', 'order']

class GoalSerializer(serializers.ModelSerializer):
    contributions = ContributionSerializer(many=True, read_only=True)
    strategy_items = StrategyItemSerializer(many=True, read_only=True)
    total_saved = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = [
            'id','owner','title','description','target_amount','monthly_target',
            'classification','start_date','end_date','created_at','completed',
            'contributions','strategy_items','total_saved','remaining','percentage'
        ]
        read_only_fields = ['owner', 'created_at', 'total_saved', 'remaining', 'percentage']

    def get_total_saved(self, obj):
        return obj.total_saved()

    def get_remaining(self, obj):
        return obj.remaining_amount()

    def get_percentage(self, obj):
        t = Decimal('0.00')
        if obj.target_amount:
            t = (obj.total_saved() / obj.target_amount) * 100
        return round(t, 2)

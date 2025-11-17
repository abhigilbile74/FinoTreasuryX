from rest_framework import viewsets, permissions
from django.db.models import Sum
from decimal import Decimal
from .models import Budget
from .serializers import BudgetSerializer
from transactions.models import Transaction

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        budgets = Budget.objects.filter(user=self.request.user)
        # Calculate spent amount for each budget from transactions
        for budget in budgets:
            self._update_spent_amount(budget)
        return budgets

    def _update_spent_amount(self, budget):
        """Calculate and update spent amount from transactions"""
        # Map category names to match between budgets and transactions
        category_map = {
            'Food & Dining': ['Food', 'Food & Dining'],
            'Food': ['Food', 'Food & Dining'],
            'Transportation': ['Transport', 'Transportation'],
            'Transport': ['Transport', 'Transportation'],
            'Shopping': ['Shopping'],
            'Entertainment': ['Entertainment'],
            'Bills': ['Bills'],
        }
        
        possible_categories = category_map.get(budget.category, [budget.category])
        spent = Transaction.objects.filter(
            user=budget.user,
            type='expense',
            category__in=possible_categories
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        budget.spent = spent
        budget.save(update_fields=['spent'])

    def perform_create(self, serializer):
        budget = serializer.save(user=self.request.user)
        self._update_spent_amount(budget)

    def perform_update(self, serializer):
        budget = serializer.save()
        self._update_spent_amount(budget)


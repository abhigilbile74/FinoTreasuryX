from django.db import models
from django.conf import settings
from decimal import Decimal

User = settings.AUTH_USER_MODEL

CLASSIFICATION_CHOICES = (
    ('short', 'Short-Term'),
    ('mid', 'Mid-Term'),
    ('long', 'Long-Term'),
)

class Goal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES, default='short')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.owner})"

    def total_saved(self):
        res = self.contributions.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        return res

    def remaining_amount(self):
        return max(self.target_amount - self.total_saved(), Decimal('0.00'))

class Contribution(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.amount} to {self.goal.title} on {self.date}"

class StrategyItem(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='strategy_items')
    method = models.CharField(max_length=200)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.method}: {self.monthly_contribution}"

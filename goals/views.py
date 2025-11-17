from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Goal, Contribution, StrategyItem
from .serializers import GoalSerializer, ContributionSerializer, StrategyItemSerializer
from .permissions import IsOwnerOrReadOnly
from decimal import Decimal
from django.db.models import Sum

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # limit to the current user's goals by default
        return Goal.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        Returns detailed progress stats for the goal:
        - total_saved, percentage, remaining, monthly_target, message
        """
        goal = self.get_object()
        total_saved = goal.total_saved()
        target = goal.target_amount or Decimal('0.00')
        if target == Decimal('0.00'):
            percentage = Decimal('0.00')
        else:
            percentage = (total_saved / target) * 100
        remaining = max(target - total_saved, Decimal('0.00'))

        # optional suggestion: compute months left if monthly_target provided
        months_left = None
        if goal.monthly_target and goal.monthly_target > 0:
            months_left = (remaining / goal.monthly_target).quantize(Decimal('1.00'))  # may be fractional

        message = ""
        if total_saved >= target and target > 0:
            message = f"🎉 CONGRATULATIONS! You’ve reached your <RuPaySymbol showLogo={false} />{int(target):,} goal! Total Saved: <RuPaySymbol showLogo={false} />{total_saved:.2f}"
        else:
            message = (
                f"Current Status: {percentage:.2f}% complete. "
                f"Saved: <RuPaySymbol showLogo={false} />{total_saved:.2f}. Remaining: <RuPaySymbol showLogo={false} />{remaining:.2f}."
            )
            if months_left is not None:
                message += f" Target Monthly Contribution: <RuPaySymbol showLogo={false} />{goal.monthly_target:.2f}. Estimated months to reach target: {months_left}."

        return Response({
            "goal_id": goal.id,
            "total_saved": total_saved,
            "percentage": round(float(percentage), 2),
            "remaining": remaining,
            "monthly_target": goal.monthly_target,
            "months_left": float(months_left) if months_left is not None else None,
            "message": message
        })

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # restrict to contributions for goals that belong to user
        return Contribution.objects.filter(goal__owner=self.request.user)

class StrategyItemViewSet(viewsets.ModelViewSet):
    queryset = StrategyItem.objects.all()
    serializer_class = StrategyItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StrategyItem.objects.filter(goal__owner=self.request.user)

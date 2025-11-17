"""
Rule-based helpers for budget and insight generation.
Keep simple, explainable rules here.
"""
from datetime import datetime

def suggest_50_30_20(income: float):
    """
    Return recommendations using 50/30/20 rule.
    """
    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2
    return {
        "income": income,
        "needs": needs,
        "wants": wants,
        "savings": savings,
        "text": f"50/30/20 on ₹{income:,.2f} → Needs: ₹{needs:,.2f}, Wants: ₹{wants:,.2f}, Savings: ₹{savings:,.2f}"
    }

def simple_rebalance_suggestion(current_alloc: dict, target_alloc: dict, threshold_pct=5):
    """
    Given current and target allocations (in percentages), suggest rebalancing if deviation > threshold_pct.
    Example:
       current_alloc = {"equity":60, "bonds":30, "gold":10}
       target_alloc = {"equity":50, "bonds":40, "gold":10}
    """
    suggestions = []
    for k, target in target_alloc.items():
        current = current_alloc.get(k, 0)
        diff = current - target
        if abs(diff) >= threshold_pct:
            action = "sell" if diff > 0 else "buy"
            suggestions.append({
                "asset": k,
                "current_pct": current,
                "target_pct": target,
                "action": action,
                "amount_pct": abs(diff)
            })
    return suggestions

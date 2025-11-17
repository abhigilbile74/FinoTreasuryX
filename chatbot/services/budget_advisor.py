from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from ..ml.rules_engine import suggest_50_30_20

def suggest_budget_changes(user):
    """
    Simple budget advisor that compares last 30 days spending to reported monthly income (if present).
    Expects UserProfile or similar to store monthly_income at user.profile.monthly_income.
    """
    Transaction = apps.get_model("transactions", "Transaction")
    now = timezone.now()
    since = now - timedelta(days=30)
    qs = Transaction.objects.filter(user=user, date__gte=since)

    total_spent = sum(float(getattr(t, "amount", 0) or 0) for t in qs)
    profile = getattr(user, "profile", None)
    income = None
    if profile and hasattr(profile, "monthly_income"):
        try:
            income = float(profile.monthly_income)
        except:
            income = None

    lines = [f"You spent ₹{total_spent:,.2f} in the last 30 days."]
    if income:
        pct = (total_spent / income) * 100 if income else 0
        lines.append(f"This is {pct:.1f}% of your reported monthly income (₹{income:,.2f}).")
        if pct > 80:
            lines.append("High spending relative to income — consider reducing wants and subscriptions. Target: increase savings by 10%.")
        elif pct > 50:
            lines.append("Moderate spending — small tweaks could improve savings.")
        else:
            lines.append("Good — spending under control relative to reported income.")
    else:
        lines.append("I don't have your monthly income. Add it to your profile for personalized advice.")
        lines.append("Use the 50/30/20 rule as a baseline:")
        sample = suggest_50_30_20(50000)  # example
        lines.append(sample["text"])
    return "\n".join(lines)

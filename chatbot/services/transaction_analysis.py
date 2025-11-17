"""
Summarize user transactions. This module assumes your `transactions` app exists
and has a Transaction model with at least fields: user, amount, date, category, merchant (optional).
If your Transaction model differs, adapt field names accordingly.
"""
from django.utils import timezone
from datetime import timedelta
from django.apps import apps

def analyze_transactions_for_user(user, days=90):
    Transaction = apps.get_model("transactions", "Transaction")
    now = timezone.now()
    since = now - timedelta(days=days)

    qs = Transaction.objects.filter(user=user, date__gte=since)
    if not qs.exists():
        return f"I couldn't find transactions in the last {days} days. Add transactions to get summaries."

    total = 0.0
    by_category = {}
    by_merchant = {}
    for t in qs:
        amt = float(getattr(t, "amount", 0) or 0)
        total += amt
        cat = getattr(t, "category", None) or "uncategorized"
        by_category[cat] = by_category.get(cat, 0) + amt
        merchant = getattr(t, "merchant", None)
        if merchant:
            by_merchant[merchant] = by_merchant.get(merchant, 0) + amt

    top_cats = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:5]
    top_merchants = sorted(by_merchant.items(), key=lambda x: x[1], reverse=True)[:5]

    lines = [f"In the last {days} days you spent ₹{total:,.2f}. Top categories:"]
    for cat, amt in top_cats:
        pct = (amt / total) * 100 if total else 0
        lines.append(f"- {cat}: ₹{amt:,.2f} ({pct:.1f}%)")
    if top_merchants:
        lines.append("Top merchants:")
        for m, amt in top_merchants:
            lines.append(f"- {m}: ₹{amt:,.2f}")
    return "\n".join(lines)

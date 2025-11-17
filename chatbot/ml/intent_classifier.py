"""
Hybrid intent classifier:
 - Simple keyword/rule based first (fast, predictable)
 - Placeholder to plug-in a persisted sklearn model (joblib) or transformer later
"""
import re
from typing import Optional

INTENT_KEYWORDS = {
    "transactions_summary": ["spent", "transactions", "where did i spend", "expenses", "expense", "spent last", "spent this"],
    "budget_advice": ["budget", "saving", "save", "savings", "overspend", "cut down", "reduce"],
    "investment": ["invest", "investment", "portfolio", "mutual fund", "sip", "etf", "stocks", "bonds"],
    "emi": ["emi", "loan", "interest rate", "installment"],
    "greeting": ["hi", "hello", "hey", "good morning", "good evening"],
    "bye": ["bye", "goodbye", "see you", "later"],
}

FLATTENED = {}
for intent, kws in INTENT_KEYWORDS.items():
    for kw in kws:
        FLATTENED[kw] = intent


def clean_text(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9\s%₹$.,]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def classify_intent(text: str) -> str:
    txt = clean_text(text)

    # exact keyword search (longer keywords first)
    keywords = sorted(FLATTENED.keys(), key=lambda x: -len(x))
    for kw in keywords:
        if kw in txt:
            return FLATTENED[kw]

    # pattern heuristics
    if any(tok in txt for tok in ["how much did i spend", "spent last", "spent in", "last month i spent"]):
        return "transactions_summary"
    if any(tok in txt for tok in ["how to save", "help me save", "save money", "savings plan"]):
        return "budget_advice"
    if any(tok in txt for tok in ["should i invest", "where to invest", "investment suggestion", "portfolio suggestion"]):
        return "investment"

    # fallback
    return "general"

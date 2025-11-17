"""
Lightweight portfolio advisor that uses historical returns from your records or
simple heuristics. This example demonstrates a mean-variance optimizer using
simulated returns if real price history isn't available.

Note: This is educational code; do not consider it financial advice.
"""
import numpy as np
from scipy.optimize import minimize

def compute_optimal_weights(mean_returns, cov_matrix, risk_free_rate=0.03):
    """
    Maximize Sharpe ratio -> minimize negative Sharpe.
    mean_returns: np.array of expected returns (annualized)
    cov_matrix: covariance matrix (annualized)
    """
    n = len(mean_returns)
    init = np.repeat(1/n, n)
    bounds = tuple((0.0, 1.0) for _ in range(n))
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    def portfolio_perf(weights):
        ret = np.dot(weights, mean_returns)
        vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = (ret - risk_free_rate) / vol if vol != 0 else 0
        return -sharpe

    result = minimize(portfolio_perf, init, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        return list(init)  # fallback to equal weights
    return list(result.x.round(4))


def portfolio_advice(user, user_message=None):
    # Simple demo assets and simulated statistics
    assets = ["Equity", "Bonds", "Gold"]
    # annual mean returns (example)
    mean_returns = np.array([0.12, 0.05, 0.06])
    # covariance (example)
    cov_matrix = np.array([
        [0.10**2, 0.10*0.04*0.2, 0.10*0.06*0.1],
        [0.10*0.04*0.2, 0.04**2, 0.04*0.06*0.05],
        [0.10*0.06*0.1, 0.04*0.06*0.05, 0.06**2]
    ])
    weights = compute_optimal_weights(mean_returns, cov_matrix)
    suggestion = {assets[i]: float(weights[i]) for i in range(len(assets))}
    lines = ["Based on a simple mean-variance optimizer (demo):"]
    for a, w in suggestion.items():
        lines.append(f"- {a}: {w*100:.1f}%")
    lines.append("This is a demo suggestion. Provide risk profile or link historical returns for better advice.")
    return "\n".join(lines)

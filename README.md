# FinoTreasuryX
The Personalized Financial Navigator (PFN) is a full personal finance app for real-time control and insights. It features a Dashboard, Analytics, a SMART Goal Tracker, and AI tools for budgeting and investment recommendations.

Personalized Financial Navigator (PFN)

🚀 Smarter Financial Management. Building Your Tomorrow, Today.

Your Financial Edge. Gain real-time visibility of your cash flow, manage liquidity, automate payments, and make data-driven decisions—all to accelerate progress toward your biggest financial goals. Securely managed, powerfully simple.

PFN is a modern, full-stack personal finance tracker designed to provide comprehensive financial visibility, advanced analytics, and personalized AI-driven advice.

✨ Features

1. Dashboard & Transactions

Overview: Real-time summary of Total Balance, Total Income, Total Expense, and Saving Rate.

Recent Transactions: Quick view of the latest financial activity.

Add Transaction: Easy form to log new income or expense, supporting various built-in categories (Food, Transport, Recharge) and the ability to add custom fields for hyper-personalized tracking.

2. Analytics Dashboard (Financial Edge)

Comprehensive financial insights and trends, allowing users to track activity across different timelines:

Timeframes: 7 Days, 30 Days, 90 Days, 365 Days, and All Time.

Insights: Spending by Category, Financial Goals Progress, Budget Utilization, and Saving Insight visualizations.

3. Goals: SMART Financial Goal Tracker

A dedicated module to define, plan, and track financial aspirations:

Goal Definition: Add Goal Statement, Classification (Short-term, Mid-term, Long-term), and Timeline.

Planning: Calculates Financial Requirements and suggests a Best Combination Strategy (Monthly Breakdown).

Tracking: Add contributions and monitor progress with a dynamic Current Progress Bar.

4. AI-Powered Chatbot

Real-time Assistance: Utilizes a Hugging Face Free LLM model trained on the user's overall transactional data and budgets.

Functionality: Provides instant, live chat answers regarding personalized financial queries (e.g., "Am I spending too much on food this month?", "How much should I allocate to my emergency fund?").

5. Investment Portfolio Recommendation

A sophisticated module leveraging machine learning algorithms trained on your financial dataset to provide actionable investment advice.

Recommendation Engine:

Qualitative Advice: E.g., "Excellent—You're saving well! Consider diversifying your portfolio with equity, bonds, and gold."

Suggested Portfolio Allocation: Provides a percentage breakdown for core asset classes (e.g., Equity 60%, Bonds 30%, Gold 10%).

AI Investment Options (Mean-Variance Demo): Shows optimized allocations based on simplified risk models (e.g., Equity: 35.0%, Bonds: 35.3%, Gold: 29.7%).

Investment Avenues: Lists practical options like Equity Mutual Funds, Debt Funds, SIPs, Fixed Deposits, and PPF.


🌐 Access the Application

- Local backend: `http://127.0.0.1:8000`
- Local frontend (Vite): `http://localhost:5173`

## Deployment (Render)

1. **Provision PostgreSQL** on Render and copy the `DATABASE_URL`.
2. **Environment variables** for the backend web service:
   ```
   DJANGO_SETTINGS_MODULE=Finance.deployment_settings
   SECRET_KEY=<secure value>
   DATABASE_URL=<render postgres url>
   FRONTEND_URL=https://finotreasuryx.onrender.com
   ALLOWED_HOSTS=finotreasuryx.onrender.com,<backend-service>.onrender.com
   ```
   Optional:
   ```
   CREATE_SUPERUSER=true
   DJANGO_SUPERUSER_USERNAME=<admin>
   DJANGO_SUPERUSER_EMAIL=<email>
   DJANGO_SUPERUSER_PASSWORD=<password>
   ```
3. **Build Command**: `./build.sh`
4. **Start Command**: `gunicorn Finance.wsgi`
5. **Static files**: WhiteNoise + `collectstatic` handled via the build script.

📝 Educational Resources

Investopedia

Khan Academy - Personal Finance

The Financial Diet

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or improvements.

📄 License

This project is licensed under the MIT License.

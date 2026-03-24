"""
Loan Affordability Analysis
Author: Shivanisri Chippa

What this script does:
  Given a customer's monthly income and expenses,
  it decides whether they can afford a loan payment.

Assumptions:
  - Month 3 income (15,000) is a one-time spike → excluded from stable average
  - A 1.25x safety buffer is applied over the loan payment
  - Expenses are treated as fixed recurring obligations
  - No credit score or existing debt data available
"""

import json
from statistics import mean


# ── INPUT DATA ────────────────────────────────────────────────
# Each entry = one month of the customer's bank statement

transaction_data = [
    {"month": 1, "income": 12000, "expenses": 8000},
    {"month": 2, "income": 6000,  "expenses": 5500},
    {"month": 3, "income": 15000, "expenses": 9000},  # one-time spike
]

LOAN_PAYMENT       = 4000   # monthly loan amount being evaluated
SPIKE_THRESHOLD    = 1.5    # income > 1.5x other months' average = spike
MIN_COVERAGE_RATIO = 1.25   # customer needs 25% buffer beyond loan payment


# ── STEP 1: FLAG INCOME SPIKES ────────────────────────────────
# A month is a spike if its income is unusually high compared
# to the average of all other months (leave-one-out check).
# Spike months are excluded from the stable income average
# so we don't overestimate what the customer normally earns.

def flag_spikes(records):
    all_incomes = [r["income"] for r in records]

    for i, record in enumerate(records):
        other_incomes    = [v for j, v in enumerate(all_incomes) if j != i]
        baseline_average = mean(other_incomes) if other_incomes else 0
        record["is_spike"] = (
            baseline_average > 0 and
            record["income"] > SPIKE_THRESHOLD * baseline_average
        )

    return records


# ── STEP 2: CALCULATE FINANCIAL METRICS ──────────────────────
# Compute two income averages:
#   raw_average_income      → simple average including all months
#   adjusted_average_income → average after removing spike months
#
# The adjusted average is used for the loan decision because
# it reflects what the customer reliably earns each month.

def calculate_metrics(records):
    all_incomes    = [r["income"]   for r in records]
    all_expenses   = [r["expenses"] for r in records]
    stable_incomes = [r["income"]   for r in records if not r["is_spike"]]

    raw_average_income      = mean(all_incomes)
    adjusted_average_income = mean(stable_incomes) if stable_incomes else raw_average_income
    average_monthly_expenses = mean(all_expenses)

    net_cash_flow    = round(adjusted_average_income - average_monthly_expenses, 2)
    cash_after_loan  = round(net_cash_flow - LOAN_PAYMENT, 2)

    return {
        "raw_average_income"      : raw_average_income,
        "adjusted_average_income" : adjusted_average_income,
        "average_monthly_expenses": average_monthly_expenses,
        "total_expenses"          : sum(all_expenses),
        "net_cash_flow"           : net_cash_flow,
        "cash_after_loan"         : cash_after_loan,
    }


# ── STEP 3: MAKE LOAN DECISION ────────────────────────────────
# The customer is approved only if their net cash flow
# covers the loan payment with the required safety buffer.
#
# Required flow = loan_payment × 1.25
# Example: loan = 4000 → customer needs at least 5000 left/month

def make_decision(net_cash_flow):
    required_flow = LOAN_PAYMENT * MIN_COVERAGE_RATIO

    if net_cash_flow >= required_flow:
        return "APPROVE", (
            f"Net cash flow ({net_cash_flow:,.0f}) covers the loan payment ({LOAN_PAYMENT:,}) "
            f"with the required {MIN_COVERAGE_RATIO}x safety buffer."
        )
    else:
        shortfall = LOAN_PAYMENT - net_cash_flow
        return "REJECT", (
            f"Net cash flow ({net_cash_flow:,.0f}) is insufficient to cover the loan payment "
            f"({LOAN_PAYMENT:,}). Shortfall: {shortfall:,.0f}. "
            f"Does not meet the {MIN_COVERAGE_RATIO}x safety buffer requirement."
        )


# ── STEP 4: BUILD JSON OUTPUT ─────────────────────────────────
# Packages everything into a clean, structured JSON report.
# This format can be consumed directly by any API or dashboard.

def build_report(records, metrics, decision, reason):
    return {
        "decision": decision,
        "decision_reason": reason,

        "summary": {
            "loan_payment_evaluated"  : LOAN_PAYMENT,
            "raw_average_income"      : metrics["raw_average_income"],
            "adjusted_average_income" : metrics["adjusted_average_income"],
            "average_monthly_expenses": metrics["average_monthly_expenses"],
            "total_expenses"          : metrics["total_expenses"],
            "net_cash_flow"           : metrics["net_cash_flow"],
            "cash_after_loan_payment" : metrics["cash_after_loan"],
        },

        "monthly_breakdown": [
            {
                "month"          : r["month"],
                "income"         : r["income"],
                "expenses"       : r["expenses"],
                "net_flow"       : r["income"] - r["expenses"],
                "is_income_spike": r["is_spike"],
                "note"           : (
                    "Excluded from adjusted average — one-time income spike"
                    if r["is_spike"] else
                    "Normal month — included in analysis"
                ),
            }
            for r in records
        ],

        "assumptions": [
            "Month 3 income treated as a one-time spike and excluded from stable average",
            "A 1.25x safety buffer is required above the loan payment for approval",
            "Expenses are assumed to be fixed recurring obligations",
            "All figures are in the same currency (USD)",
        ],

        "additional_info_needed_for_real_decision": [
            "Credit score and existing debt obligations (DTI ratio)",
            "Employment type — salaried vs freelance vs business owner",
            "At least 6-12 months of transaction history for reliability",
            "Emergency savings and liquidity buffer",
            "Nature of any income spikes (bonus, asset sale, inheritance?)",
        ],
    }


# ── MAIN: RUN THE FULL PIPELINE ───────────────────────────────

records          = flag_spikes(transaction_data)
metrics          = calculate_metrics(records)
decision, reason = make_decision(metrics["net_cash_flow"])
report           = build_report(records, metrics, decision, reason)

print(json.dumps(report, indent=2))

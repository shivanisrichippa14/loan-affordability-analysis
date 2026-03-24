# Loan Affordability Analysis

A simple Python script that evaluates whether a customer can afford a fixed monthly loan payment — based on their income and expense history.

---

## Problem Statement

Given a customer's 3-month transaction history, determine whether they can sustainably afford a **$4,000/month** loan payment.

| Month | Income | Expenses |
|-------|--------|----------|
| 1     | $12,000 | $8,000  |
| 2     | $6,000  | $5,500  |
| 3     | $15,000 | $9,000  |

> **Key challenge:** Month 3 contains a one-time income spike (e.g. a bonus or asset sale).  
> A naive average would overestimate the customer's real earning capacity.

---

## Approach

Rather than a simple average, the script uses a **leave-one-out spike detection** algorithm:

- For each month, compute the average of all *other* months
- If a month's income exceeds **1.5×** that baseline → flagged as a spike
- Spikes are excluded from the adjusted income average used in the decision

This ensures the loan decision reflects what the customer **reliably earns**, not what they earned once.

---

## Decision Logic

```
Approved  if:  adjusted net cash flow  >=  loan payment × 1.25
Rejected  if:  adjusted net cash flow  <   loan payment × 1.25
```

The **1.25× safety buffer** accounts for unexpected expenses — a standard practice in conservative lending.

---

## How It Works — Step by Step

```
1. flag_spikes()       →  detect and mark one-time income anomalies
2. calculate_metrics() →  compute raw average, adjusted average, net cash flow
3. make_decision()     →  apply coverage ratio rule → APPROVE or REJECT
4. build_report()      →  package all results as structured JSON
```

---

## Output (JSON)

```json
{
  "decision": "REJECT",
  "decision_reason": "Net cash flow (1,500) is insufficient...",
  "summary": {
    "loan_payment_evaluated": 4000,
    "raw_average_income": 11000,
    "adjusted_average_income": 9000,
    "average_monthly_expenses": 7500,
    "total_expenses": 22500,
    "net_cash_flow": 1500,
    "cash_after_loan_payment": -2500
  },
  "monthly_breakdown": [...],
  "assumptions": [...],
  "additional_info_needed_for_real_decision": [...]
}
```

---

## Run the Script

```bash
python loan_analysis.py
```

No external libraries required — uses Python standard library only (`json`, `statistics`).

---

## Assumptions

- Month 3 income ($15,000) is treated as a one-time spike and excluded from the stable average
- A **1.25× safety buffer** is required above the loan payment for approval
- Expenses are assumed to be fixed recurring obligations
- All figures are in USD
- No credit score, existing debt, or savings data was available for this analysis

## What Additional Data Would Improve This Decision

- Credit score and existing debt obligations (DTI ratio)
- Employment type — salaried vs freelance vs business owner
- At least 6–12 months of transaction history
- Emergency savings and liquidity buffer
- Nature of any income spikes (bonus, asset sale, inheritance?)

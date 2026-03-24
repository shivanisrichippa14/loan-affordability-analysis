# Loan Affordability Analysis

This project evaluates whether a customer can afford a fixed monthly loan payment based on their income and expenses.

## 📊 Problem Statement

Given a 3-month transaction dataset:
- Income and expenses per month
- Determine if the customer can afford a $4000/month loan

## 🧠 Approach

The solution focuses on:
- Monthly cash flow analysis
- Income stability evaluation
- Conservative financial decision-making

## ⚙️ Key Features

- Calculates monthly net cash flow
- Handles income anomalies (one-time spike)
- Computes:
  - Simple average income
  - Adjusted average income (excluding spike)
- Makes loan approval decision based on consistency

## 📈 Decision Logic

Loan is approved only if:
- All months can sustain the loan payment
- Income is stable and reliable

## 🚨 Key Insight

Month 3 contains a one-time income spike, which is excluded from decision-making to ensure realistic financial assessment.

## ▶️ Run the Script

```bash
python main.py

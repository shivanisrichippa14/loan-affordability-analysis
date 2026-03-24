def calculate_net_cashflow(income, expenses):
    return [i - e for i, e in zip(income, expenses)]


def calculate_average_income(income, exclude_spike=False):
    if exclude_spike:
        # Remove the highest value (assumed spike)
        adjusted_income = sorted(income)[:-1]
        return sum(adjusted_income) / len(adjusted_income)
    return sum(income) / len(income)


def loan_decision(net_cashflow, loan_amount):
    # Check if all months can handle the loan
    for cash in net_cashflow:
        if cash < loan_amount:
            return "Reject"
    return "Approve"


def main():
    income = [12000, 6000, 15000]
    expenses = [8000, 5500, 9000]
    loan_amount = 4000

    net_cashflow = calculate_net_cashflow(income, expenses)
    avg_income_simple = calculate_average_income(income)
    avg_income_adjusted = calculate_average_income(income, exclude_spike=True)
    total_expenses = sum(expenses)

    decision = loan_decision(net_cashflow, loan_amount)

    result = {
        "monthly_breakdown": [
            {"month": i+1, "income": income[i], "expenses": expenses[i], "net": net_cashflow[i]}
            for i in range(len(income))
        ],
        "average_income_simple": avg_income_simple,
        "average_income_adjusted": avg_income_adjusted,
        "total_expenses": total_expenses,
        "net_cashflow": net_cashflow,
        "loan_amount": loan_amount,
        "final_decision": decision,
        "note": "Decision based on consistency of cash flow and conservative income estimation."
    }

    print(result)


if __name__ == "__main__":
    main()

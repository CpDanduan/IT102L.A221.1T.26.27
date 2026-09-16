from ukayclick_storage import load_expenses, save_expenses, timestamp

def record_expense(category, description, amount):
    if float(amount) <= 0:
        return False, "Expense must be greater than ₱0.00."
    expenses = load_expenses()
    expense = {
        "timestamp": timestamp(),
        "expense_id": f"EX{len(expenses)+1:05d}",
        "category": category,
        "description": description.strip() or category,
        "amount": round(float(amount), 2)
    }
    expenses.append(expense)
    save_expenses(expenses)
    return True, "Expense recorded."

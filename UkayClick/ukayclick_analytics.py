from collections import defaultdict
from datetime import datetime, date

def sales_summary(transactions, expenses):
    today = date.today().isoformat()
    today_sales = sum(float(x["total"]) for x in transactions if x["timestamp"].startswith(today))
    total_sales = sum(float(x["total"]) for x in transactions)
    total_expenses = sum(float(x["amount"]) for x in expenses)
    count = len(transactions)
    return {
        "today_sales": today_sales,
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "net_cash_flow": total_sales - total_expenses,
        "transaction_count": count,
        "average_sale": total_sales / count if count else 0
    }

def inventory_summary(inventory):
    return {
        "total_quantity": sum(int(x["quantity"]) for x in inventory),
        "unique_items": len(inventory),
        "low_stock": sum(1 for x in inventory if int(x["quantity"]) <= 2),
        "inventory_value": sum(float(x["price"]) * int(x["quantity"]) for x in inventory)
    }

def demand_forecast(transactions, inventory):
    sold = defaultdict(int)
    for t in transactions:
        sold[t["item_id"]] += int(t["quantity"])

    results = []
    for item in inventory:
        units = sold[item["item_id"]]
        # Simple prototype heuristic: classify demand using historical units sold.
        if units >= 10:
            level = "High"
        elif units >= 5:
            level = "Medium"
        else:
            level = "Low"
        results.append({
            "Item ID": item["item_id"],
            "Product": item["name"],
            "Current Stock": item["quantity"],
            "Units Sold": units,
            "Demand Estimate": level,
            "Suggested Action": "Consider restocking" if level == "High" else ("Monitor" if level == "Medium" else "Review sales")
        })
    return results

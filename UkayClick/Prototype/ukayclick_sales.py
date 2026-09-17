from ukayclick_storage import load_inventory, save_inventory, load_transactions, save_transactions, timestamp

def process_sale(item_id, quantity, customer, payment, customer_payment):
    inventory = load_inventory()
    item = next((x for x in inventory if x["item_id"] == item_id), None)
    quantity = int(quantity)
    if item is None:
        return False, "Product not found."
    if quantity <= 0 or quantity > item["quantity"]:
        return False, "Invalid quantity."
    total = round(item["price"] * quantity, 2)
    item["quantity"] -= quantity
    change = customer_payment - total if payment == "Cash" else 0.0
    save_inventory(inventory)

    transactions = load_transactions()
    sale = {
        "timestamp": timestamp(),
        "transaction_id": f"TX{len(transactions)+1:05d}",
        "item_id": item["item_id"],
        "product": item["name"],
        "category": item["category"],
        "quantity": quantity,
        "unit_price": item["price"],
        "total": total,
        "customer": customer.strip() or "Walk-in",
        "payment": payment,
        "change": change
    }
    transactions.append(sale)
    save_transactions(transactions)
    return True, sale

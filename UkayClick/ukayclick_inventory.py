from ukayclick_storage import load_inventory, save_inventory

def add_item(name, category, price, quantity, cost):
    name = name.strip()
    if not name:
        return False, "Product name is required."
    items = load_inventory()
    next_id = max([int(x["item_id"][2:]) for x in items] or [0]) + 1
    items.append({
        "item_id": f"UK{next_id:04d}",
        "name": name,
        "category": category,
        "price": round(float(price), 2),
        "quantity": int(quantity),
        "cost": round(float(cost), 2)
    })
    save_inventory(items)
    return True, "Product added."

def update_item(item_id, price, quantity):
    items = load_inventory()
    for item in items:
        if item["item_id"] == item_id:
            item["price"] = round(float(price), 2)
            item["quantity"] = int(quantity)
            save_inventory(items)
            return True, "Product updated."
    return False, "Product not found."

def delete_item(item_id):
    items = load_inventory()
    new_items = [x for x in items if x["item_id"] != item_id]
    if len(new_items) == len(items):
        return False, "Product not found."
    save_inventory(new_items)
    return True, "Product deleted."

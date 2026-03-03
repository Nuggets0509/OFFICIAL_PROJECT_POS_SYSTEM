import json
import random
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data.json")
CATEGORY_ORDER = ["Food", "Soft Drinks", "Pasta", "Desserts"]


def to_non_negative_int(value, default=0):
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if cleaned == "":
            return default
        value = cleaned
    try:
        number = int(float(value))
        return number if number >= 0 else default
    except (TypeError, ValueError):
        return default


def normalize_items(items):
    normalized = []
    for item in items:
        raw_quantity = item.get("quantity")
        if raw_quantity is None:
            raw_quantity = item.get("qty", item.get("stock", item.get("in_stock", 0)))
        normalized.append(
            {
                "id": to_non_negative_int(item.get("id")),
                "name": str(item.get("name", "")).strip(),
                "price": float(item.get("price", 0)),
                "quantity": to_non_negative_int(raw_quantity),
                "category": item.get("category", ""),
            }
        )
    return normalized


def load_data():
    if not DATA_FILE.exists():
        return {"items": []}
    with DATA_FILE.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    data["items"] = normalize_items(data.get("items", []))
    return data


def save_data(items):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump({"items": items}, f, indent=4)


def banner():
    print("_" * 60)
    print("\nWelcome to PAPI PEDROS PIZZERIA")
    print("_" * 60)
    print(
        """\n1. Show All Products
\n2. Sales
\n3. Add Products
\n4. Remove Products
\n5. Update Products
\n6. Exit"""
    )
    print("_" * 60)


def display_all(items):
    categorized = {category: [] for category in CATEGORY_ORDER}
    for item in items:
        category = get_category(item)
        categorized[category].append(item)

    for category in CATEGORY_ORDER:
        if not categorized[category]:
            continue
        print(f"\n{category}")
        print(f"{'SNO':<5}{'Product':<35}{'Price':>10}")
        for item in categorized[category]:
            print(f"{item['id']:<5}{item['name']:<35}P {item['price']:>7.2f}")


def get_category(item):
    raw_category = str(item.get("category", "")).strip().lower()
    if raw_category in {"food", "soft drinks", "pasta", "desserts"}:
        return raw_category.title() if raw_category != "soft drinks" else "Soft Drinks"

    name = item.get("name", "").lower()
    if any(word in name for word in ("drink", "coke", "tea", "juice", "soda", "water")):
        return "Soft Drinks"
    if any(word in name for word in ("spaghetti", "fettuccine", "penne", "lasagna", "pasta")):
        return "Pasta"
    if any(word in name for word in ("tiramisu", "dessert", "cake", "brownie", "ice cream", "cookie")):
        return "Desserts"
    return "Food"


def order_summary(products, amounts, total, quantities):
    print("-" * 60)
    print("\t\tPAPI PEDROS PIZZERIA")
    print("-" * 60)
    print(f"Order Summary\t\tDate:{datetime.now()}")
    print(" ")
    print("Product name\t\t\tQuantity\tPrice")
    print("-" * 60)
    for i in range(len(products)):
        print(f"{products[i]}\t\t  {quantities[i]}\t\tP {amounts[i]:.2f}")
    print("-" * 60)
    print(f"Total Payment Amount:\t\t\t\tP {total:.2f}")


def generate_bill(total, products, amounts, quantities, change, amount_received):
    print("-" * 60)
    print("\n\tPAPI PEDROS PIZZERIA")
    print("-" * 60)
    print(f"Bill:{int(random.random() * 100000)} \t\tDate:{datetime.now()}")
    print(" ")
    print("Product name\t\t\tQuantity\tPrice")
    print("-" * 60)
    for i in range(len(products)):
        print(f"{products[i]}\t\t  {quantities[i]}\t\tP {amounts[i]:.2f}")
    print("-" * 60)
    print(f"Total Bill Amount:\t\t\t\tP {total:.2f}")
    print(f"  Amount Received:\t\t\t\tP {amount_received:.2f}")
    print(f"           Change:\t\t\t\tP {change:.2f}")


def get_item_by_id(items, item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def parse_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid whole number.")


def parse_quantity(prompt, min_value=0):
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            number = float(raw)
        except ValueError:
            print("Please enter a valid quantity (example: 5, 5.0, 1,000).")
            continue

        if not number.is_integer():
            print("Quantity must be a whole number.")
            continue

        quantity = int(number)
        if quantity < min_value:
            if min_value == 1:
                print("Quantity must be at least 1.")
            else:
                print(f"Quantity must be at least {min_value}.")
            continue
        return quantity


def parse_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def run_sales(items):
    cart = []
    requested_by_id = {}
    total_bill = 0.0

    display_all(items)
    print("Enter product IDs separated by comma (example: 1,2,3). Enter 0 to finish.")

    while True:
        order_raw = input("What do you want to buy today? ").strip()
        if order_raw == "0":
            break

        try:
            order_ids = [int(x.strip()) for x in order_raw.split(",") if x.strip()]
        except ValueError:
            print("Invalid input. Use IDs like: 1,2,3")
            continue

        for order_id in order_ids:
            item = get_item_by_id(items, order_id)
            if item is None:
                print(f"Item ID {order_id} not found.")
                continue

            quantity = parse_quantity(f"Please enter quantity for {item['name']}: ", min_value=1)
            requested_by_id[order_id] = requested_by_id.get(order_id, 0) + quantity
            amount = item["price"] * quantity
            cart.append((item["name"], quantity, amount))
            total_bill += amount

    if not cart:
        print("No items ordered.")
        return

    names = [x[0] for x in cart]
    quantities = [x[1] for x in cart]
    amounts = [x[2] for x in cart]
    order_summary(names, amounts, total_bill, quantities)

    conf = input("Please confirm your order (Y/N): ").strip().upper()
    if conf != "Y":
        print("Order cancelled.")
        return

    for item_id, qty in requested_by_id.items():
        item = get_item_by_id(items, item_id)
        if item is not None:
            item["quantity"] -= qty

    member = input("Do you have membership (Y/N): ").strip().upper()
    if member == "Y":
        total_bill *= 0.9

    while True:
        payment = parse_float("Amount Received: ")
        if payment < total_bill:
            print(f"Insufficient amount. You still need P {total_bill - payment:.2f}")
            continue
        break

    change = payment - total_bill
    generate_bill(total_bill, names, amounts, quantities, change, payment)
    save_data(items)
    print(" ")
    print("Thank you for shopping with us :)")


def add_product(items):
    name = input("Enter item name: ").strip()
    item_price = parse_float("Enter the price: ")
    item_quantity = parse_quantity("Enter the quantity: ", min_value=0)
    next_id = max((item["id"] for item in items), default=0) + 1

    items.append(
        {
            "id": next_id,
            "name": name,
            "price": item_price,
            "quantity": item_quantity,
        }
    )
    save_data(items)
    print("Item added.")


def remove_product(items):
    if not items:
        print("No products to remove.")
        return
    display_all(items)
    remove_id = parse_int("Enter item ID to remove: ")
    item = get_item_by_id(items, remove_id)
    if item is None:
        print("Item not found.")
        return

    items.remove(item)
    save_data(items)
    print("Item removed.")


def update_product(items):
    if not items:
        print("No products to update.")
        return
    display_all(items)
    update_id = parse_int("Enter item ID to update: ")
    item = get_item_by_id(items, update_id)
    if item is None:
        print("Item not found.")
        return

    new_name = input(f"Enter new name [{item['name']}]: ").strip()
    new_price_raw = input(f"Enter new price [{item['price']}]: ").strip()
    new_qty_raw = input(f"Enter new quantity [{item['quantity']}]: ").strip()

    if new_name:
        item["name"] = new_name
    if new_price_raw:
        try:
            item["price"] = float(new_price_raw)
        except ValueError:
            print("Invalid price. Keeping old value.")
    if new_qty_raw:
        try:
            parsed_qty = int(float(new_qty_raw.replace(",", "")))
            if not float(new_qty_raw.replace(",", "")).is_integer():
                raise ValueError
            if parsed_qty < 0:
                print("Invalid quantity. Keeping old value.")
            else:
                item["quantity"] = parsed_qty
        except ValueError:
            print("Invalid quantity. Keeping old value.")

    save_data(items)
    print("Item updated.")


def main():
    data = load_data()
    items = data.get("items", [])

    while True:
        banner()
        choice = parse_int("Please enter your option: ")

        if choice == 1:
            display_all(items)
        elif choice == 2:
            run_sales(items)
        elif choice == 3:
            add_product(items)
        elif choice == 4:
            remove_product(items)
        elif choice == 5:
            update_product(items)
        elif choice == 6:
            save_data(items)
            print("Thank you")
            sys.exit(0)
        else:
            print("Invalid choice. Please choose 1-6.")


if __name__ == "__main__":
    main()

import json
import random
import sys
import time
import os
from datetime import datetime
from pathlib import Path

# Get the folder where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Food menu
DATA_FILE = Path("data.json")
CATEGORY_ORDER = ["Food", "Soft Drinks", "Pasta", "Desserts"]

# Builds accounts file path in the same folders as the script
ACCOUNTS = os.path.join(SCRIPT_DIR, "accounts.txt")

def checkUsername(user):
    sameUsername = False
    with open(ACCOUNTS, "r") as f: # Open accounts file:
        lines = f.readlines()

    for line in lines:
        # Get each usernames
        prevUsername = line.split(",")
        if prevUsername[0] == user:
            prevUsername = ""
            sameUsername = True
            break
        else:
            sameUsername = False

    if sameUsername:
        return True
    else:
        return False
    
def create():
    print("\n")
    invalidUsername = True # Determines if user entered a name same to the person
    invalidPw = True       # Determines if password has been entered

    while invalidUsername:
        username = ""
        prevUsername = "" # Scans the previous

        while True:
            username = input("Enter your choses Papi-zza username: ") # Make account if the name does not match any previous usernames
            if username == '':
                pass
            elif username.count(" ") > 0:
                print("Your Papi-zza username must have no spaces.")
            else:
                break
        
        if checkUsername(username) == True: # Check if username has already been used
                print("This Papi-zza username has already been used. Please choose another")
                restart = True
                invalidUsername = True

        else:
                invalidUsername = False
                restart = False

        if restart == True:
            continue

        while invalidPw:
            password = input("Enter your password: ")
            if password == "":
                pass
            else:
                invalidPw = False

        f = open(ACCOUNTS, "a")
        f.write(f"\n{username}, {password}")
        print("Accounts successfully created!")
        f.close()
    return True


def login(): # Enters menu
    f = open(ACCOUNTS, "r") # Open Accounts File
    lines = f.readlines()
    f.close()

    password = ""
    scanUsername = ""
    invalidUsername = True

    # Ask for username and password
    while invalidUsername:
        option1 = ""
        username = input("\nEnter your username: ")
        if checkUsername(username): # See if username has been registered
            for line in lines:
                scanUsername = line.split(",")
                if scanUsername[0] == username:
                    userPass = scanUsername[1].strip()
                    invalidUsername = False

        else: 
            while True:
                option1 = input("Username is not found. Enter your username again (y) or go back to menu(n)? ").lower()
                if option1 == 'y':
                    break
                elif option1 == 'n':
                    return False
                
    while password != userPass.strip(): #Get password after username is found
        option2 = ""
        password = input(f"Enter password for {username}: ").strip()
        if password != userPass:
            while True:
                option2 = input("You entered the wrong password. Try again (y) or go back to menu (n)? ")
                if option2 == 'y':
                    break
                elif option2 == 'n':
                    return False
        else:
            print("Login Successful!")
            return True

def start_login_menu(): # Login menu
    while True:
        print("\n" + "=" * 60)
        print("PAPI PEDRO'S PIZZERIA - ACCOUNT")
        print("=" * 60)
        print("1: Create your Papi-zza Account")
        print("2: Login to your Papi-zza Account")
        print("3: Exit")

        option = ""
        while option not in ("1", "2", "3"):
            option = input("Please select an option: ").strip()

        if option == "1":
            if create():
                print("Redirecting to the menu...")
                time.sleep(2)
                return True
        elif option == "2":
            if login():
                print("Redirecting to the menu...")
                time.sleep(2)
                return True
        else:
            print("Thank you for visiting Papi Pedro's Pizzeria!")
            time.sleep(2)
            return False

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


def normalize_items(items): # Items 
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
\n3. Exit"""
    )
    print("_" * 60)


def display_all(items): # Display all items of the food from the data.json
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


def get_category(item): # Separate the food into Categories
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


def order_summary(products, amounts, total, quantities): # Summary of food, with checkout
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


def display_current_order(requested_by_id, items): #Display all the current orders
    print("\n" + "=" * 60)
    print("CURRENT ORDER")
    print("=" * 60)
    print(f"{'ID':<5}{'Product':<30}{'Qty':>6}{'Amount':>15}")
    running_total = 0.0

    for item_id in sorted(requested_by_id):
        qty = requested_by_id[item_id]
        item = get_item_by_id(items, item_id)
        if item is None:
            continue
        amount = item["price"] * qty
        running_total += amount
        print(f"{item_id:<5}{item['name']:<30}{qty:>6}  P {amount:>10.2f}")

    print("-" * 60)
    print(f"{'Subtotal':>45}: P {running_total:>10.2f}")
    print("=" * 60)


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
            display_current_order(requested_by_id, items)

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
   
    print("\nOrder confirmed! Sending your request to Papi's Kitchen...")
    time.sleep(1)
    
    start_prep_timer(requested_by_id.keys(), items)
    
    
    print(" ")
    print("Thank you for shopping with us :)")
    sys.exit(0)

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
            save_data(items)
            print("Thank you")
            sys.exit(0)
        else:
            print("Invalid choice. Please choose 1-6.")


if __name__ == "__main__":
    if start_login_menu():
        main()
    else:
        sys.exit(0)


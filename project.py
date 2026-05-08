"""
 STARLIGHT GENERAL SHOP - Modern POS System
author: Lukas (Perplexity Enhanced)
date: 2026-04-15
Tech: Python 3 | Interactive CLI | Real-time Inventory | Cash Receipts
"""

import os
import time
from datetime import datetime
from tabulate import tabulate  # pip install tabulate (optional, fallback included)

# Enhanced Product Database
products = [
    {"id": 1, "name": "Milk", "price": 100.0, "quantity": 23, "category": "Dairy", "active": True},
    {"id": 2, "name": "Bread", "price": 30.0, "quantity": 29, "category": "Bakery", "active": True},
    {"id": 3, "name": "Eggs (6)", "price": 30.0, "quantity": 12, "category": "Dairy", "active": True},
    {"id": 4, "name": "Chocolate Bar", "price": 66.0, "quantity": 10, "category": "Snacks", "active": True},
    {"id": 5, "name": "Rice (1kg)", "price": 120.0, "quantity": 25, "category": "Grains", "active": True}
]

LOW_STOCK_THRESHOLD = 5
SALES_HISTORY = []  # Persistent sales log


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║   STARLIGHT GENERAL SHOP - NextGen POS System                    ║
║   {} | 💻 Modern Inventory & Sales Management                   ║
╚══════════════════════════════════════════════════════════════════════╝
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


def main_menu():
    options = [
        " 1. Product Catalogue",
        " 2. Add Product",
        " 3. Remove Product",
        "4. Search Products",
        " 5. Low Stock Alert",
        " 6. New Sale (Basket Checkout)",
        " 7. Sales History",
        " 8. Exit"
    ]
    print("\n".join(options))
    print("\n" + "━" * 55)


def display_catalogue():
    active_products = [p for p in products if p["active"]]
    if not active_products:
        print(" No active products!")
        return

    table_data = []
    for p in active_products:
        status = "" if p["quantity"] > LOW_STOCK_THRESHOLD else "⚠️"
        table_data.append([
            p["id"], p["name"], f"Ksh.{p['price']:.2f}",
            p["quantity"], p["category"], status
        ])

    headers = ["ID", "Product", "Price", "Stock", "Category", "Status"]
    print(tabulate(table_data, headers, tablefmt="grid"))
    print(f"\n Tip: Use Product ID for faster checkout!")


def add_product():
    print("\n➕ NEW PRODUCT")
    print("━" * 40)
    pid = max(p["id"] for p in products) + 1 if products else 1
    name = input("  Product Name: ").strip().title()
    if not name:
        print(" Invalid name!")
        return

    try:
        price = float(input("  Price (Ksh): "))
        qty = int(input("  Initial Stock: "))
        cat = input("  Category: ").strip().title()
    except ValueError:
        print(" Invalid input!")
        return

    products.append({
        "id": pid, "name": name, "price": price,
        "quantity": qty, "category": cat, "active": True
    })
    print(f"\n{name} (ID:{pid}) added successfully!")


def remove_product():
    print("\n DEACTIVATE PRODUCT")
    display_catalogue()
    try:
        pid = int(input("\nEnter Product ID to deactivate: "))
        for p in products:
            if p["id"] == pid and p["active"]:
                p["active"] = False
                print(f"\n {p['name']} deactivated.")
                return
        print(" Product not found or already inactive!")
    except ValueError:
        print(" Invalid ID!")


def search_product():
    keyword = input("\n🔍 Search (name/category): ").strip().lower()
    matches = [p for p in products if p["active"] and keyword in p["name"].lower() or keyword in p["category"].lower()]

    if matches:
        table_data = [[p["id"], p["name"], f"Ksh.{p['price']:.2f}", p["quantity"]] for p in matches]
        print(tabulate(table_data, ["ID", "Name", "Price", "Stock"], tablefmt="grid"))
    else:
        print(" No matches found!")


def low_stock_alert():
    low_items = [p for p in products if p["active"] and 0 < p["quantity"] <= LOW_STOCK_THRESHOLD]
    if low_items:
        print("\n⚠️  LOW STOCK ITEMS:")
        for item in low_items:
            print(f"  • {item['name']}: {item['quantity']} left")
    else:
        print("\n All stock levels OK!")


def record_sale():
    basket = []
    subtotal = 0.0
    customer_name = input("\n Customer Name (optional): ").strip().title() or "Cash Customer"

    print("\nBUILDING BASKET")
    display_catalogue()

    while True:
        print(f"\nBasket Subtotal: Ksh.{subtotal:.2f}")
        action = input("\nProduct ID/name or 'done': ").strip().lower()

        if action == 'done':
            break

        found = False
        # Try ID first, then name
        for p in products:
            if p["active"]:
                if str(p["id"]) == action or action in p["name"].lower():
                    try:
                        qty = int(input(f"  Qty for {p['name']}: "))
                        if qty > 0 and p["quantity"] >= qty:
                            line_total = p["price"] * qty
                            basket.append({"name": p["name"], "price": p["price"], "qty": qty, "total": line_total})
                            subtotal += line_total
                            p["quantity"] -= qty
                            print(f"  ✓ Added {qty}x {p['name']}")
                            found = True
                        else:
                            print(f"   Only {p['quantity']} available")
                    except ValueError:
                        print("   Invalid quantity")
                    break

        if not found:
            print("   Product not found")

    if not basket:
        print("No sale recorded.")
        return

    # Payment Processing
    print("\nCHECKOUT")
    print(tabulate([[i["name"], i["qty"], f"Ksh.{i['total']:.2f}"] for i in basket],
                   ["Item", "Qty", "Total"], tablefmt="grid"))

    print(f"\n{'SUBTOTAL:':<15} Ksh.{subtotal:.2f}")

    try:
        payment = float(input("💰 Cash Tendered: Ksh. "))
        if payment < subtotal:
            print(f" Short by Ksh.{subtotal - payment:.2f}")
            return

        change = payment - subtotal

        # Record Sale
        sale_record = {
            "timestamp": datetime.now().isoformat(),
            "customer": customer_name,
            "items": len(basket),
            "subtotal": subtotal,
            "payment": payment,
            "change": change,
            "basket": basket
        }
        SALES_HISTORY.append(sale_record)

        # Print Receipt
        print("\n" + "═" * 70)
        print(f"{'RECEIPT':^70}")
        print("═" * 70)
        print(f"Customer: {customer_name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        for item in basket:
            print(f"{item['name']:<25} x{item['qty']:>2}  Ksh.{item['total']:>7.2f}")
        print("-" * 70)
        print(f"{'SUBTOTAL:':<25} {'Ksh.':<8} {subtotal:>7.2f}")
        print(f"{'PAYMENT:':<25} {'Ksh.':<8} {payment:>7.2f}")
        print(f"{'CHANGE:':<25} {'Ksh.':<8} {change:>7.2f}")
        print("═" * 70)
        print(" Thank you for shopping at Starlight! ")
        print("═" * 70)

    except ValueError:
        print(" Invalid payment!")


def sales_history():
    if not SALES_HISTORY:
        print("\n📊 No sales recorded yet!")
        return

    print("\n📊 RECENT SALES")
    recent = SALES_HISTORY[-5:]  # Last 5
    for i, sale in enumerate(recent, 1):
        print(f"\nSale #{i} | {sale['timestamp'][:16]}")
        print(f"  Customer: {sale['customer']} | Items: {sale['items']}")
        print(f"  Total: Ksh.{sale['subtotal']:.2f} | Paid: Ksh.{sale['payment']:.2f}")


def run_shop():
    while True:
        banner()
        main_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            display_catalogue()
        elif choice == "2":
            add_product()
        elif choice == "3":
            remove_product()
        elif choice == "4":
            search_product()
        elif choice == "5":
            low_stock_alert()
        elif choice == "6":
            record_sale()
        elif choice == "7":
            sales_history()
        elif choice == "8":
            print("\n Goodbye! Starlight Shop closed.")
            break
        else:
            print("\n Invalid! Press Enter...")

        input("\n⏎ Press Enter to continue...")
        time.sleep(0.5)


if __name__ == "__main__":
    print(" Starting Starlight POS System...")
    run_shop()
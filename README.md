"""
Daily Finance Calculator - Modern Personal Finance Tool (Fixed & Shop-Integrated)
Author: Laven Flacko (Perplexity Assisted)
Date: 2026-05-08
Purpose: Calculate interest, EMI, track monthly budget + shop sales sync, CSV export.
Tech: Pure Python 3 | No external libs | Error-handled CLI
"""

import csv
from datetime import datetime
import os

# File for budget transactions
BUDGET_FILE = "budget_log.csv"
SHOP_SALES_FILE = "sales.csv"  # From your Starlight POS


def calculate_simple_interest(p, r, t):
    """Simple Interest: SI = P * R * T / 100"""
    return (p * r * t) / 100


def calculate_compound_interest(p, r, t):
    """Compound Interest: CI = P * (1 + R/100)^T - P"""
    return p * (1 + r / 100) ** t - p


def calculate_emi(p, r, t):
    """EMI for loan: Monthly payment formula."""
    r_monthly = r / 12 / 100
    n_months = t * 12
    if r_monthly == 0:
        return p / n_months
    emi = p * r_monthly * (1 + r_monthly) ** n_months / ((1 + r_monthly) ** n_months - 1)
    return emi


def safe_float_input(prompt, allow_negative=False):
    """Get float input with validation."""
    while True:
        try:
            value = float(input(prompt).strip())
            if not allow_negative and value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Enter a valid number (e.g., 10000).")


def budget_add_income():
    amount = safe_float_input("Enter income amount (Ksh): ")
    desc = input("Description (e.g., Salary): ").strip() or "Income"
    log_transaction("Income", desc, amount)
    print(f"Added Ksh {amount:,.2f} income.")


def budget_add_expense():
    amount = safe_float_input("Enter expense amount (Ksh): ")
    desc = input("Description (e.g., Rent): ").strip() or "Expense"
    log_transaction("Expense", desc, -amount)
    print(f"Added Ksh {amount:,.2f} expense.")


def sync_shop_sales():
    """Import daily sales from shop POS as income."""
    if not os.path.exists(SHOP_SALES_FILE):
        print("No sales.csv found. Run your shop POS first.")
        return
    total_sales = 0
    try:
        with open(SHOP_SALES_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header if present
            for row in reader:
                if len(row) >= 2 and row[1].replace(".", "").replace("-", "").isdigit():
                    total_sales += float(row[1])
    except Exception as e:
        print(f"Error reading {SHOP_SALES_FILE}: {e}")
        return
    if total_sales > 0:
        log_transaction("Shop Sales", f"Daily from {SHOP_SALES_FILE}", total_sales)
        print(f"Synced Ksh {total_sales:,.2f} shop sales.")
    else:
        print("No valid sales data found in sales.csv.")


def log_transaction(category, description, amount):
    """Log to CSV with timestamp."""
    row = [datetime.now().strftime("%Y-%m-%d %H:%M"), category, description, f"{amount:.2f}"]
    file_exists = os.path.exists(BUDGET_FILE)
    with open(BUDGET_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Category", "Description", "Amount"])
        writer.writerow(row)


def view_budget():
    """Show current balance from CSV."""
    if not os.path.exists(BUDGET_FILE):
        print("No transactions yet. Add some!")
        return
    total = 0.0
    print("\nRecent Transactions:")
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header safely
            for row in reader:
                if len(row) >= 4:
                    try:
                        amt = float(row[3])
                        total += amt
                        print(f"{row[0]} | {row[1]}: {row[2]} | Ksh {amt:,.2f}")
                    except ValueError:
                        continue  # Skip bad rows
    except Exception as e:
        print(f"Error reading budget file: {e}")
        return
    print(f"\nCurrent Balance: Ksh {total:,.2f}")
    if total < 5000:
        print("⚠️  Low balance alert! Consider cutting expenses.")


def export_budget():
    """CSV is already exported. View or open in Excel."""
    print(f"Budget log saved to {BUDGET_FILE}. Open in Excel!")


def main_menu():
    while True:
        print("\n=== Daily Finance Calculator ===")
        print("1. Simple Interest")
        print("2. Compound Interest")
        print("3. Loan EMI")
        print("4. Add Income")
        print("5. Add Expense")
        print("6. View Budget")
        print("7. Sync Shop Sales")  # New: Links to your POS
        print("8. Export CSV")
        print("0. Exit")

         choice = input("Choose (0-8): ").strip()

        if choice == "1":
            p = safe_float_input("Principal (Ksh): ")
            r = safe_float_input("Rate (%): ")
            t = safe_float_input("Time (years): ")
            si = calculate_simple_interest(p, r, t)
            print(f"Simple Interest: Ksh {si:,.2f}")

        elif choice == "2":
            p = safe_float_input("Principal (Ksh): ")
            r = safe_float_input("Rate (%): ")
            t = safe_float_input("Time (years): ")
            ci = calculate_compound_interest(p, r, t)
            print(f"Compound Interest: Ksh {ci:,.2f}")

        elif choice == "3":
            p = safe_float_input("Loan Amount (Ksh): ")
            r = safe_float_input("Annual Rate (%): ")
            t = safe_float_input("Tenure (years): ")
            emi = calculate_emi(p, r, t)
            print(f"Monthly EMI: Ksh {emi:,.2f}")

        elif choice == "4":
            budget_add_income()

        elif choice == "5":
            budget_add_expense()

        elif choice == "6":
            view_budget()

        elif choice == "7":
            sync_shop_sales()

        elif choice == "8":
            export_budget()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()

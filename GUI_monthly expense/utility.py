from datetime import date
import pandas as pd
def total_expense_current_month():
    today = date.today()
    month_year = today.strftime("%b").upper() + str(today.year)  # e.g., NOV2025
    filename = f"{month_year}.csv"
    
    try:
        data = pd.read_csv(filename)
        # Make sure amount column is numeric
        data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
        total = data["amount"].sum()
        print(f"💰 Total expense for {month_year}: ₹{total}")
    except FileNotFoundError:
        print(f"No expenses found for {month_year}")
    print("""
============================================================
          """)
import os
import pandas as pd
from datetime import date,datetime
def write_to_current_csv(expense_date,category,description,amount):
    today = date.today()
    month_year = today.strftime("%b").upper() + str(today.year)
    filename = rf"{month_year}.csv"

    # Create the row data
    new_row = pd.DataFrame([{
        "date": expense_date,
        "category": category,
        "description": description,
        "amount": amount}])

    # If CSV exists → append
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"📌 Added to {filename}")
    
    else:
        # Else → create new CSV
        new_row.to_csv(filename, index=False)
        print(f"📁 Created {filename} and saved first entry")

def read_from_freq_csv():
    d_freq = pd.read_csv(r"frequent.csv")
    return(d_freq)

def write_to_freq_csv(category, description, amount, month_df):
    count = len(month_df[
        (month_df["category"] == category) & 
        (month_df["description"] == description)
    ])

    if count <= 4:
        return  # not frequent yet
    
    # Load frequent.csv
    freq_df = pd.read_csv(r"frequent.csv")

    # Check if already present
    exists = ((freq_df["category"] == category) &
              (freq_df["description"] == description)).any()

    if exists:
        return
    
    # Add new frequent item
    new_row = {"category": category, "description": description, "amount": amount}
    freq_df = pd.concat([freq_df, pd.DataFrame([new_row])], ignore_index=True)

    freq_df.to_csv(r"frequent.csv", index=False)


def read_from_given_month(month_year):
    filename = rf"{month_year}.csv"   # Example: JAN2025.csv
    
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            print(f"Loaded data from {filename}")
            return df
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return pd.DataFrame()
    else:
        print(f"No data found for {month_year}. Returning empty DataFrame.")
        return pd.DataFrame()

def write_to_csv(expense_date, category, description, amount):
    # Convert string to datetime object
    date_obj = datetime.strptime(expense_date, "%d-%m-%Y")
    
    # Filename based on month and year of the expense
    month_year = date_obj.strftime("%b").upper() + str(date_obj.year)
    filename = rf"{month_year}.csv"
    
    # Create a new row as a DataFrame
    new_row = pd.DataFrame([{
        "date": expense_date,
        "category": category,
        "description": description,
        "amount": amount
    }])
    
    # If CSV exists → append
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"📌 Added to {filename}")
    
    else:
        # Else → create new CSV
        new_row.to_csv(filename, index=False)
        print(f"📁 Created {filename} and saved first entry")


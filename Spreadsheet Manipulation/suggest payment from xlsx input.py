import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import csv

#opens excel input file and recommends payment based on it

def open_file():
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        process_excel(file_path)

def process_excel(file_path):
    # Read the Financial Projection sheet
    df = pd.read_excel(file_path, sheet_name="Financial Projection")

    # Extract necessary columns
    calendar = df["Calendar"]
    rolling_cash = df["Rolling Cash"]

    # Get debt names and ask for interest rates
    debt_names = [col for col in df.columns if "Student Loan" in col or "Credit Card" in col]
    interest_rates = {}
    
    for debt in debt_names:
        interest_rates[debt] = float(input(f"Enter interest rate for {debt}: "))

    # Calculate optimal payment strategy
    payment_strategy = {}
    for date, cash in zip(calendar, rolling_cash):
        if cash <= 0:
            break  # Stop calculating payments if rolling cash is zero or negative

        payment_date = pd.to_datetime(date) + pd.DateOffset(days=14)  # Assume payment on the 15th of the month
        payment_date = payment_date.strftime("%m/%d/%Y")

        payment_strategy[date] = {"Rolling Cash Before Payment": cash}
        for debt in debt_names:
            payment = min(cash, interest_rates[debt] * cash)
            payment_strategy[date][debt] = payment
            cash -= payment

        payment_strategy[date]["Rolling Cash After Payment"] = cash

    # Write payment strategy to CSV
    csv_file_path = os.path.join(os.path.dirname(file_path), "payment_strategy.csv")
    with open(csv_file_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["Date", "Rolling Cash Before Payment"] + debt_names + ["Rolling Cash After Payment"])
        # Write data
        for date, payments in payment_strategy.items():
            writer.writerow([date, payments["Rolling Cash Before Payment"]] + [payments[debt] for debt in debt_names] + [payments["Rolling Cash After Payment"]])

    print(f"Payment strategy has been saved to: {csv_file_path}")

# GUI setup
root = tk.Tk()
root.title("Debt Payment Calculator")

# Button to open file
open_button = tk.Button(root, text="Open Excel File", command=open_file)
open_button.pack(pady=20)

# Run GUI loop
root.mainloop()

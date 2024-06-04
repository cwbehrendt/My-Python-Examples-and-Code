import tkinter as tk

#code that prompts user for information and calculates a debt payment strategy from it
#i lost interest in this one, it doesn't look great GUI-wise

def store_data(entry, variable):
    value = entry.get()
    try:
        variable.set(float(value))
    except ValueError:
        variable.set(0.0)


def calculate_financial_info():
    rolling_cash_values = []
    credit_card_debt_values = []
    
    rolling_cash = starting_cash.get()
    cc_debt_total = cc_debt_total_var.get()
    cc_apr_interest = cc_apr_interest_var.get()

    
    cc_monthly_interest = cc_apr_interest / 12 / 100

    for month in range(1, 13):
        
        sugpay = max(0, rolling_cash * 0.25) if cc_debt_total > 0 else 0

        
        sugpay = min(sugpay, cc_debt_total)

        
        rolling_cash -= sugpay

        
        cc_debt_total = max(0, cc_debt_total * (1 + cc_monthly_interest) - sugpay)
        credit_card_debt_values.append((month, round(cc_debt_total, 2)))

        
        recommended_payment = rolling_cash + paycheck.get() - bills.get() - sugpay
        rolling_cash = rolling_cash + paycheck.get() - bills.get()
        rolling_cash_values.append((month, round(rolling_cash, 2), round(recommended_payment, 2)))

    display_financial_info(rolling_cash_values, credit_card_debt_values)


def display_financial_info(rolling_cash_values, credit_card_debt_values):
    result_window = tk.Toplevel(root)
    result_window.title("Financial Information")

    result_window.geometry("400x400")  

    for (month, rolling_cash, recommended_payment), (_, credit_card_debt) in zip(rolling_cash_values, credit_card_debt_values):
        label = tk.Label(result_window, text=f"Month {month}:\nRolling Cash: {rolling_cash}\nCredit Card Debt: {credit_card_debt}\nRecommended Monthly Debt Payment: {round(rolling_cash * 0.25, 2)}")
        label.pack(pady=10)


root = tk.Tk()
root.title("Financial Information")


cc_debt_total_var = tk.DoubleVar()
cc_apr_interest_var = tk.DoubleVar()

cc_frame = tk.Frame(root)
cc_frame.pack(pady=10)

cc_label = tk.Label(cc_frame, text="Enter Total Credit Card Debt:")
cc_label.pack(side=tk.LEFT)

cc_entry_total = tk.Entry(cc_frame, textvariable=cc_debt_total_var)
cc_entry_total.pack(side=tk.LEFT, padx=10)

cc_label_interest = tk.Label(cc_frame, text="Enter Credit Card APR Interest:")
cc_label_interest.pack(side=tk.LEFT)

cc_entry_interest = tk.Entry(cc_frame, textvariable=cc_apr_interest_var)
cc_entry_interest.pack(side=tk.LEFT)


paycheck = tk.DoubleVar()

paycheck_frame = tk.Frame(root)
paycheck_frame.pack(pady=10)

paycheck_label = tk.Label(paycheck_frame, text="Enter Net Monthly Take Home:")
paycheck_label.pack(side=tk.LEFT)

paycheck_entry = tk.Entry(paycheck_frame, textvariable=paycheck)
paycheck_entry.pack(side=tk.LEFT)


bills = tk.DoubleVar()

bills_frame = tk.Frame(root)
bills_frame.pack(pady=10)

bills_label = tk.Label(bills_frame, text="Enter Total Monthly Bills (excluding credit card payments):")
bills_label.pack(side=tk.LEFT)

bills_entry = tk.Entry(bills_frame, textvariable=bills)
bills_entry.pack(side=tk.LEFT)


rolling_cash = tk.DoubleVar(value=0.0)


starting_cash = tk.DoubleVar()

cash_frame = tk.Frame(root)
cash_frame.pack(pady=10)

cash_label = tk.Label(cash_frame, text="Enter Total Liquid Cash:")
cash_label.pack(side=tk.LEFT)

cash_entry = tk.Entry(cash_frame, textvariable=starting_cash)
cash_entry.pack(side=tk.LEFT)


calculate_button = tk.Button(root, text="Calculate Financial Info", command=calculate_financial_info)
calculate_button.pack(pady=10)


root.mainloop()

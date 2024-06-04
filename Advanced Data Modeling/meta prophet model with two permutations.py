import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def load_and_forecast():
    def select_holidays_with_impact():
        holidays = [
            "New Year's Day", "Martin Luther King Jr. Day", "Washington's Birthday",
            "Memorial Day", "Independence Day", "Labor Day", "Columbus Day",
            "Veterans Day", "Thanksgiving Day", "Christmas Day", "Cinco de Mayo"
        ]

        selected_holidays = {}

        def on_select():
            popup.quit()

        def select_button(button):
            button.config(bg="green")
            button.config(state="disabled")

        def create_button(holiday):
            button = tk.Button(popup, text=holiday, command=lambda: show_entry_popup(holiday, button))
            button.pack()
            return button

        def show_entry_popup(holiday, button):
            entry_popup = tk.Toplevel(popup)
            entry_popup.title(holiday)
            tk.Label(entry_popup, text=f"As a percentage between 1 and 100, how much of your sales does {holiday} make up? ").pack()
            entry = tk.Entry(entry_popup)
            entry.pack()

            def on_ok():
                impact = entry.get()
                try:
                    impact = float(impact)
                    if 1 <= impact <= 100:
                        selected_holidays[holiday] = impact
                        entry_popup.destroy()
                        select_button(button)
                    else:
                        messagebox.showerror("Error", "Please enter a percentage between 1 and 100.")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number.")

            tk.Button(entry_popup, text="OK", command=on_ok).pack()

        popup = tk.Toplevel()
        popup.title("Select US Holidays with Impact")

        tk.Label(popup, text="Select US Holidays that impact your product:").pack()

        buttons = [create_button(holiday) for holiday in holidays]

        tk.Button(popup, text="Finish", command=on_select).pack()

        popup.mainloop()
        popup.destroy()

        return selected_holidays

    def add_additional_regressor():
        additional_regressors = {}

        def on_select():
            popup.quit()

        popup = tk.Toplevel()
        popup.title("Add Additional Regressor")

        tk.Label(popup, text="Add Sale Period:").pack()

        def add_regressor():
            date = date_entry.get()
            impact = impact_entry.get()
            try:
                impact = float(impact)
                additional_regressors[date] = impact
                print(f"Sale period added: {date} with impact {impact}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for impact.")

        tk.Label(popup, text="Sale Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(popup)
        date_entry.pack()

        tk.Label(popup, text="Impact Percentage (>= 0):").pack()
        impact_entry = tk.Entry(popup)
        impact_entry.pack()

        tk.Button(popup, text="Add Sale Period", command=add_regressor).pack()
        tk.Button(popup, text="Finish", command=on_select).pack()

        popup.mainloop()
        popup.destroy()

        return additional_regressors

    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    df = pd.read_csv(file_path)

    if 'ds' not in df.columns or 'y' not in df.columns or 'Division' not in df.columns:
        messagebox.showerror("Error", "CSV must contain 'ds', 'y', and 'Division' columns.")
        return

    
    output_dir = os.path.join(os.path.dirname(file_path), 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    selected_holidays = select_holidays_with_impact()
    additional_regressors = add_additional_regressor()

    for division in df['Division'].unique():
        division_df = df[df['Division'] == division]

        model = Prophet()

        if "Cinco de Mayo" in selected_holidays:
            cinco_de_mayo_dates = pd.DataFrame({
                'holiday': 'Cinco de Mayo',
                'ds': pd.to_datetime([
                    '2023-05-05', '2024-05-05', '2025-05-05', '2026-05-05',
                    '2027-05-05', '2028-05-05', '2029-05-05', '2030-05-05'
                ]),
                'lower_window': 0,
                'upper_window': 1,
            })
            model.holidays = pd.concat((model.holidays, cinco_de_mayo_dates))

        if selected_holidays:
            holidays_df = model.train_holiday_names
            if holidays_df is not None:
                holidays_to_remove = [holiday for holiday in holidays_df if holiday not in selected_holidays]
                model.holidays = model.holidays[~model.holidays['holiday'].isin(holidays_to_remove)]

        model.fit(division_df)

        future = model.make_future_dataframe(periods=24*30, freq='D')

        for date, impact in additional_regressors.items():
            future[date] = impact

        forecast = model.predict(future)
        forecast['Division'] = division

        fig = model.plot(forecast)
        plt.title(f"Forecast for Division: {division}")

        
        plot_file_name = f"{division.replace(' ', '_')}_forecast.png"
        plot_save_path = os.path.join(output_dir, plot_file_name)
        fig.savefig(plot_save_path)
        plt.close(fig)
        print(f"Forecast plot for Division {division} saved to {plot_save_path}")

        
        division_file_name = f"{division.replace(' ', '_')}_forecast.csv"
        data_save_path = os.path.join(output_dir, division_file_name)
        forecast.to_csv(data_save_path, index=False)
        print(f"Predictions for Division {division} saved to {data_save_path}")

root = tk.Tk()
root.withdraw()

load_and_forecast()

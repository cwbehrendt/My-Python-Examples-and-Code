import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import os
import warnings
import holidays
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

    import holidays

    def smooth_outliers(df, window=7):
        """
        Smooths outliers in the dataframe by replacing values beyond the IQR with the median of surrounding values.
        """
        df['y_smoothed'] = df['y']
        for i in range(len(df)):
            window_data = df['y'].iloc[max(0, i-window):min(len(df), i+window+1)]
            median = window_data.median()
            q1 = window_data.quantile(0.25)
            q3 = window_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            if df['y'].iloc[i] < lower_bound:
                df.at[i, 'y_smoothed'] = lower_bound
            elif df['y'].iloc[i] > upper_bound:
                df.at[i, 'y_smoothed'] = upper_bound

        return df



    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    df = pd.read_csv(file_path)

    if 'ds' not in df.columns or 'y' not in df.columns or 'Division' not in df.columns or 'Product' not in df.columns:
        messagebox.showerror("Error", "CSV must contain 'ds', 'y', 'Division', and 'Product' columns.")
        return

    
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')

    
    df.dropna(subset=['ds', 'y'], inplace=True)

    
    output_dir = os.path.join(os.path.dirname(file_path), 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    selected_holidays = select_holidays_with_impact()
    additional_regressors = add_additional_regressor()

    for division in df['Division'].unique():
        for product in df[df['Division'] == division]['Product'].unique():
            product_df = df[(df['Division'] == division) & (df['Product'] == product)]

            
            product_df = product_df.groupby('ds').agg({'y': 'sum'}).reset_index()

            
            product_df.set_index('ds', inplace=True)
            product_df = product_df.resample('W').sum().reset_index()

            
            product_df = smooth_outliers(product_df)

            
            q1 = product_df['y_smoothed'].quantile(0.25)
            q3 = product_df['y_smoothed'].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            
            if selected_holidays:
                holiday_dates = pd.to_datetime([holiday for holiday in selected_holidays.keys()])
                for date in holiday_dates:
                    mask = (product_df['ds'] >= (date - pd.Timedelta(days=7))) & (product_df['ds'] <= (date + pd.Timedelta(days=7)))
                    holiday_data = product_df.loc[mask, 'y']
                    if len(holiday_data) > 0:
                        median_value = holiday_data.median()
                        iqr = holiday_data.quantile(0.75) - holiday_data.quantile(0.25)
                        lower_bound = median_value - 1.5 * iqr
                        upper_bound = median_value + 1.5 * iqr
                        product_df.loc[mask & (product_df['y'] > upper_bound), 'y'] = median_value

            
            if product_df.shape[0] < 2:
                print(f"Skipping Division {division}, Product {product} due to insufficient data.")
                continue

            
            seasonal_periods = min(52, max(2, product_df.shape[0] // 2))

            
            for i in range(1, len(product_df) - 1):
                if product_df['y_smoothed'].iloc[i] > upper_bound:
                    product_df.at[i, 'y_smoothed'] = (product_df['y_smoothed'].iloc[i-1] + product_df['y_smoothed'].iloc[i+1]) / 2


            
            try:
                model = ExponentialSmoothing(
                    product_df['y_smoothed'],
                    trend='add',
                    seasonal='add',
                    seasonal_periods=seasonal_periods
                ).fit()
            except ValueError as e:
                print(f"Error fitting model for Division {division}, Product {product}: {e}")
                continue

            future_dates = pd.date_range(start=product_df['ds'].max(), periods=26, freq='W')
            forecast = model.forecast(steps=26)
            forecast_df = pd.DataFrame({'ds': future_dates, 'y': forecast})


            
            forecast_df = pd.DataFrame({'ds': future_dates, 'y': forecast})

            
            historical_avg = product_df['y_smoothed'].mean()

            
            forecast_df['y'] = forecast_df['y'].apply(lambda x: max(x, historical_avg))

            forecast_df['Division'] = division
            forecast_df['Product'] = product

            
            fig, ax = plt.subplots()
            product_df.plot(x='ds', y='y_smoothed', ax=ax, label='Observed', title=f"Forecast for Division: {division}, Product: {product}")
            forecast_df.plot(x='ds', y='y', ax=ax, label='Forecast')

            
            ax.axhline(y=q1, color='r', linestyle='--', label='Q1 (25th percentile)')
            ax.axhline(y=q3, color='g', linestyle='--', label='Q3 (75th percentile)')
            ax.axhline(y=lower_bound, color='b', linestyle=':', label='Lower bound (Q1 - 1.5*IQR)')
            ax.axhline(y=upper_bound, color='b', linestyle=':', label='Upper bound (Q3 + 1.5*IQR)')

            
            ax.axhline(y=historical_avg, color='m', linestyle='--', label='Historical Average (Baseline)')


            plt.legend()

            
            plot_file_name = f"{division.replace(' ', '_')}_{product.replace(' ', '_')}_forecast.png"
            plot_save_path = os.path.join(output_dir, plot_file_name)
            fig.savefig(plot_save_path)
            plt.close(fig)
            print(f"Forecast plot for Division {division}, Product {product} saved to {plot_save_path}")

            
            product_file_name = f"{division.replace(' ', '_')}_{product.replace(' ', '_')}_forecast.csv"
            data_save_path = os.path.join(output_dir, product_file_name)
            forecast_df.to_csv(data_save_path, index=False)
            print(f"Predictions for Division {division}, Product {product} saved to {data_save_path}")

root = tk.Tk()
root.withdraw()

load_and_forecast()

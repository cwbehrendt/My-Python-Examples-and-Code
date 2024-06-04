import tkinter as tk
from tkinter import filedialog
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
import os

def select_file():
    file_path = filedialog.askopenfilename(title="Select a CSV file")
    if file_path:
        run_holt_winters(file_path)

def run_holt_winters(file_path):
    
    data = pd.read_csv(file_path)

    
    data['ds'] = pd.to_datetime(data['ds'])
    data.set_index('ds', inplace=True)

    
    model = ExponentialSmoothing(data, seasonal_periods=12, trend='add', seasonal='add')

    
    fitted_model = model.fit()

    
    future = pd.date_range(start=data.index[-1], periods=12, freq='M')

    
    forecast = fitted_model.forecast(steps=12)

    
    output_path = os.path.dirname(file_path)
    forecast_df = pd.DataFrame({'ds': future, 'forecast': forecast})
    forecast_df.to_csv(os.path.join(output_path, 'holt_winters_forecast.csv'), index=False)

    print("Holt-Winters forecast completed and saved.")


root = tk.Tk()
root.withdraw()  


select_file()


root.mainloop()

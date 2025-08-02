from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

# Ensure the uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    try:
        # Get parameters from the form
        start_date = request.form.get('start_date', '2023-01-01')
        periods = int(request.form.get('periods', 365))
        seasonality = request.form.get('seasonality', 'weekly')
        trend_strength = float(request.form.get('trend_strength', 0.5))
        noise_level = float(request.form.get('noise_level', 0.2))
        
        # Generate the dataset
        df = generate_time_series_data(start_date, periods, seasonality, trend_strength, noise_level)
        
        # Save to CSV
        csv_path = os.path.join('uploads', 'sales_data.csv')
        df.to_csv(csv_path, index=False)
        
        # Create preview charts
        preview_img = create_preview_chart(df)
        
        return jsonify({
            'status': 'success',
            'message': 'Dataset generated successfully!',
            'file_path': 'uploads/sales_data.csv',
            'preview': preview_img,
            'row_count': len(df)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/download_dataset')
def download_dataset():
    file_path = os.path.join('uploads', 'sales_data.csv')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        file_path = os.path.join('uploads', 'sales_data.csv')
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'No dataset found. Please generate one first.'})
        
        # Read the dataset
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Get forecast parameters
        forecast_periods = int(request.form.get('forecast_periods', 30))
        
        # Perform the forecast
        result = perform_forecast(df, forecast_periods)
        
        return jsonify({
            'status': 'success',
            'forecast_chart': result['chart'],
            'metrics': result['metrics']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def generate_time_series_data(start_date, periods, seasonality, trend_strength, noise_level):
    """Generate synthetic time series data for sales forecasting"""
    # Create date range
    dates = pd.date_range(start=start_date, periods=periods)
    
    # Create base trend (linear increase)
    trend = np.linspace(100, 100 + (100 * trend_strength), periods)
    
    # Add seasonality
    if seasonality == 'weekly':
        # Weekly pattern (weekends have higher sales)
        day_of_week = dates.dayofweek
        seasonal = np.zeros(periods)
        seasonal[day_of_week == 5] = 30  # Saturday
        seasonal[day_of_week == 6] = 40  # Sunday
        seasonal[day_of_week == 4] = 20  # Friday
    elif seasonality == 'monthly':
        # Monthly pattern (higher sales at month end)
        day_of_month = dates.day
        days_in_month = dates.daysinmonth
        seasonal = 30 * (day_of_month / days_in_month)
    else:  # yearly
        # Yearly pattern (higher sales in summer and holiday season)
        month = dates.month
        seasonal = np.zeros(periods)
        # Summer peak (June-August)
        seasonal[(month >= 6) & (month <= 8)] = 30
        # Holiday season peak (November-December)
        seasonal[(month >= 11) & (month <= 12)] = 40
    
    # Add noise
    noise = np.random.normal(0, noise_level * 100, periods)
    
    # Combine components
    sales = trend + seasonal + noise
    sales = np.maximum(sales, 0)  # Ensure no negative sales
    
    # Create DataFrame
    df = pd.DataFrame({'date': dates, 'sales': sales})
    
    # Add some special events (like promotions or holidays)
    special_events = np.random.choice(periods, size=int(periods * 0.05), replace=False)
    df.loc[special_events, 'sales'] *= np.random.uniform(1.2, 1.5, size=len(special_events))
    
    return df

def create_preview_chart(df):
    """Create a preview chart of the generated data"""
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['sales'], color='#E63946')
    plt.title('Generated Sales Data')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    return base64.b64encode(image_png).decode('utf-8')

def perform_forecast(df, forecast_periods):
    """Perform time series forecasting on the dataset"""
    # Fit ARIMA model
    model = ARIMA(df['sales'], order=(5, 1, 0))
    model_fit = model.fit()
    
    # Forecast future values
    forecast = model_fit.forecast(steps=forecast_periods)
    
    # Create forecast dates
    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_periods)
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast})
    
    # Create the chart
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['sales'], label='Historical', color='#2A9D8F')
    plt.plot(forecast_df['date'], forecast_df['forecast'], label='Forecast', color='#E76F51', linestyle='--')
    plt.fill_between(forecast_df['date'], 
                    forecast_df['forecast'] - forecast_df['forecast'].std(), 
                    forecast_df['forecast'] + forecast_df['forecast'].std(), 
                    color='#E76F51', alpha=0.2)
    plt.title('Sales Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    # Calculate some metrics
    mse = ((df['sales'].iloc[-forecast_periods:].values - forecast[:forecast_periods]) ** 2).mean()
    mae = np.abs(df['sales'].iloc[-forecast_periods:].values - forecast[:forecast_periods]).mean()
    
    return {
        'chart': base64.b64encode(image_png).decode('utf-8'),
        'metrics': {
            'mse': float(mse),
            'mae': float(mae)
        }
    }

if __name__ == '__main__':
    app.run(debug=True)

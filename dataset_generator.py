import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import os

def generate_sales_data(
    start_date='2023-01-01',
    periods=365,
    seasonality='weekly',
    trend_strength=0.5,
    noise_level=0.2,
    output_file='sales_data.csv'
):
    """
    Generate a synthetic time series dataset for sales forecasting
    
    Parameters:
    -----------
    start_date : str
        Starting date in YYYY-MM-DD format
    periods : int
        Number of days to generate
    seasonality : str
        Type of seasonality pattern ('weekly', 'monthly', or 'yearly')
    trend_strength : float
        Strength of the upward trend (0.0 to 1.0)
    noise_level : float
        Amount of random noise to add (0.0 to 1.0)
    output_file : str
        Path to save the CSV file
    """
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
    df = pd.DataFrame({
        'date': dates,
        'sales': sales
    })
    
    # Add some special events (like promotions or holidays)
    special_events = np.random.choice(periods, size=int(periods * 0.05), replace=False)
    df.loc[special_events, 'sales'] *= np.random.uniform(1.2, 1.5, size=len(special_events))
    
    # Add product categories with different characteristics
    categories = ['Electronics', 'Clothing', 'Food', 'Home Goods']
    for category in categories:
        # Create unique pattern for each category
        cat_trend = trend * np.random.uniform(0.6, 1.4)
        cat_seasonal = seasonal * np.random.uniform(0.8, 1.2)
        cat_noise = np.random.normal(0, noise_level * 80, periods)
        cat_sales = cat_trend + cat_seasonal + cat_noise
        cat_sales = np.maximum(cat_sales, 0)
        
        # Add to dataframe
        df[f'{category.lower()}_sales'] = cat_sales.round(2)
    
    # Round the main sales column
    df['sales'] = df['sales'].round(2)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Dataset generated and saved to {output_file}")
    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic sales time series data")
    parser.add_argument("--start_date", default="2023-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--periods", type=int, default=365, help="Number of days to generate")
    parser.add_argument("--seasonality", default="weekly", choices=["weekly", "monthly", "yearly"], help="Seasonality pattern")
    parser.add_argument("--trend_strength", type=float, default=0.5, help="Trend strength (0.0-1.0)")
    parser.add_argument("--noise_level", type=float, default=0.2, help="Noise level (0.0-1.0)")
    parser.add_argument("--output", default="sales_data.csv", help="Output file path")
    
    args = parser.parse_args()
    
    generate_sales_data(
        start_date=args.start_date,
        periods=args.periods,
        seasonality=args.seasonality,
        trend_strength=args.trend_strength,
        noise_level=args.noise_level,
        output_file=args.output
    )

import pandas as pd

def total_sales_by_region(df):
    """Calculate total sales per region."""
    return df.groupby('region')['monthly_amount'].sum().reset_index()

def monthly_sales_trend(df):
    """Calculate monthly sales trend."""
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    return df.groupby('month')['monthly_amount'].sum().reset_index()

def top_performing_region(df):
    """Identify the top-performing region based on total sales."""
    total_sales = total_sales_by_region(df)
    return total_sales.sort_values(by='monthly_amount', ascending=False).head(1)

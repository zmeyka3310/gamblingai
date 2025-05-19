import pandas as pd
from io import StringIO

predicted_data = """
04/30/2025 104.47
04/29/2025 107.67
04/28/2025 109.69
04/25/2025 106.85
04/24/2025 103.475
04/23/2025 104.52
04/22/2025 98.78
04/21/2025 98.77
04/17/2025 104.45
04/16/2025 104.55
04/15/2025 110.97
04/14/2025 114.11
04/11/2025 108.50
04/10/2025 109.37
04/09/2025 98.89
04/08/2025 103.805
04/07/2025 87.46
04/04/2025 98.91
04/03/2025 103.51
04/02/2025 107.29
04/01/2025 108.515
"""

actual_data = """
04/01/2025 121.0013427734375
04/02/2025 120.65498352050781
04/03/2025 120.45703125
04/04/2025 117.12093353271484
04/07/2025 118.44160461425781
04/08/2025 114.17628479003906
04/09/2025 112.90482330322266
04/10/2025 110.2186508178711
04/11/2025 107.59619140625
04/14/2025 106.88749694824219
04/15/2025 104.2472915649414
04/16/2025 107.0707778930664
04/17/2025 105.49090576171875
04/21/2025 106.66587829589844
04/22/2025 105.98575592041016
04/23/2025 109.67232513427734
04/24/2025 111.70716857910156
04/25/2025 109.78287506103516
04/28/2025 111.16947174072266
04/29/2025 109.30767822265625
04/30/2025 108.38706970214844
"""

# Read data into DataFrames
predicted_df = pd.read_csv(StringIO(predicted_data), sep='\s+', names=['Date', 'Predicted_Price'])
actual_df = pd.read_csv(StringIO(actual_data), sep='\s+', names=['Date', 'Actual_Price'])

# Convert 'Date' to datetime objects
predicted_df['Date'] = pd.to_datetime(predicted_df['Date'], format='%m/%d/%Y')
actual_df['Date'] = pd.to_datetime(actual_df['Date'], format='%m/%d/%Y')

# Sort DataFrames by date (important for calculating returns)
predicted_df = predicted_df.sort_values(by='Date').reset_index(drop=True)
actual_df = actual_df.sort_values(by='Date').reset_index(drop=True)

# Merge the DataFrames based on 'Date'
df = pd.merge(predicted_df, actual_df, on='Date', how='inner')

# Calculate Returns
df['Old_Price'] = df['Actual_Price'].shift(1)  # Get the previous day's actual price
df = df.dropna()  # remove the first row which will have a NaN value for Old_Price

df['Actual_Return'] = (df['Actual_Price'] / df['Old_Price'] - 1.0)
df['Forecast_Return'] = (df['Predicted_Price'] / df['Old_Price'] - 1.0)

# Define the Universe (Let's assume all days are in the universe)
df['Universe'] = True  # All stocks are in the universe
df['Weight_Simple'] = df['Universe'].astype(int) # weight is 1 if in universe, 0 otherwise

# Print the resulting DataFrame
print(df)


# Example of how to access specific data
# print(df[['Date', 'Actual_Return', 'Forecast_Return', 'Weight_Simple']]) #Display a subset of the columns

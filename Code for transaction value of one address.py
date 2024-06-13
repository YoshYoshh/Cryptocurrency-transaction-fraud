import pandas as pd
import requests
import matplotlib.pyplot as plt
from colorama import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def fetch_data(address):
    # We don't show our actual API key for security purposes
    api_key = # API key
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'

    response = requests.get(url)
    data = response.json()

    # Check if the response is successful
    if data['status'] == '1':
        transactions = data['result']
    else:
        print('Error fetching data:', data['message'])
        transactions = []

    # Convert the transactions list to a Pandas DataFrame
    df = pd.DataFrame(transactions)

    # Check and display the columns to ensure 'value' is present
    print(Fore.BLUE + "\nChecking and displaying the columns to ensure 'value' is present\n" + Style.RESET_ALL)
    print(df.columns)

    # Display the first few rows to inspect the data
    print(Fore.BLUE + "\nDisplaying the first few rows to inspect the data\n" + Style.RESET_ALL)
    print(df.head())

    # Convert relevant columns to numeric types
    df['blockNumber'] = pd.to_numeric(df['blockNumber'])
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')

    # Convert 'value' column to numeric, invalid parsing will be set as NaN
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['value'].fillna(0, inplace=True)  # Handle NaN values
    df['gas'] = pd.to_numeric(df['gas'], errors='coerce')
    df['gasPrice'] = pd.to_numeric(df['gasPrice'], errors='coerce')
    df['gasUsed'] = pd.to_numeric(df['gasUsed'], errors='coerce')

    # Handle NaN values in other columns if necessary
    df.fillna(0, inplace=True)

    # Display the updated DataFrame structure
    print(Fore.BLUE + "\nDisplaying the updated DataFrame structure\n" + Style.RESET_ALL)
    print(df.dtypes)
    print("\n")
    print(df.describe())
    print(Fore.BLUE + "\nTransaction's values data overview :\n" + Style.RESET_ALL)
    print(df['value'].describe())

    # Set the timestamp as the index
    df.set_index('timeStamp', inplace=True)

    # Ensure there are no negative or extremely high values due to errors
    df = df[df['value'] >= 0]
    
    # Plot transaction value over time
    plt.figure(figsize=(12, 6))
    df['value'].plot()
    
    # title='Transaction Value Over Time'
    plt.xlabel('Time')
    plt.ylabel('Transaction Value')
    plt.grid(True)
    plt.show()


# Fetch and plot data for the given Ethereum address
fetch_data('0x27899ffaCe558bdE9F284Ba5C8c91ec79EE60FD6')

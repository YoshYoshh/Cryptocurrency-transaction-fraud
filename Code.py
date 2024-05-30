import pandas as pd
import requests
import matplotlib.pyplot as plt

def fetch_data(address):
    # Replace with your Etherscan API key
    api_key = 'JQMQPR9JN9NHN47PFIJHYRX57Z4BSFEPCB'
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

    # Display the columns to ensure 'value' is present
    print(df.columns)

    # Display the first few rows to inspect the data
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
    print(df.dtypes)
    print(df.describe())
    
    # Plot transaction value over time
    df.set_index('timeStamp', inplace=True)
    df['value'].plot(title='Transaction Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Transaction Value (in Wei)')
    plt.show()


print(fetch_data('0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'))

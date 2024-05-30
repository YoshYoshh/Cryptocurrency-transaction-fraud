import pandas as pd
import requests

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

    # Display the first few rows of the DataFrame
    print(df.head())

print(fetch_data('0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae')

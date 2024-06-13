import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from time import sleep


def fetch_block_number(api_key, timestamp):
   url = f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={api_key}'
   response = requests.get(url)
   data = response.json()
   if data['status'] == '1':
       return int(data['result'])
   else:
       raise ValueError(f"Error fetching block number: {data['message']}")


def fetch_transactions_for_block(api_key, block_number):
   url = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={hex(block_number)}&boolean=true&apikey={api_key}'
   response = requests.get(url)
   data = response.json()
   if 'result' in data and data['result'] is not None:
       block_time = int(data['result']['timestamp'], 16)
       transaction_count = len(data['result']['transactions'])
       return block_time, transaction_count
   else:
       print(f"Skipping block {block_number}, data not found.")
       return None, 0


def fetch_total_transactions(api_key, start_block, end_block, batch_size=100):
   transactions_by_day = {}
   for block_number in range(start_block, end_block + 1, batch_size):
       batch_end_block = min(block_number + batch_size - 1, end_block)
       print(f"Processing blocks from {block_number} to {batch_end_block}")


       for bn in range(block_number, batch_end_block + 1):
           block_time, transaction_count = fetch_transactions_for_block(api_key, bn)
           if block_time:
               date = datetime.utcfromtimestamp(block_time).strftime('%Y-%m-%d')
               if date not in transactions_by_day:
                   transactions_by_day[date] = 0
               transactions_by_day[date] += transaction_count

       # Sleep to avoid hitting the rate limit
       sleep(1)

   return transactions_by_day


def main():
   # We don't show our actual API key for security purposes
   api_key = #API KEY


   # Define the start and end timestamps for January 2024
   start_timestamp = int(datetime(2024, 1, 1).timestamp())
   end_timestamp = int(datetime(2024, 2, 1).timestamp())


   # Fetch the block numbers corresponding to the start and end timestamps
   start_block = fetch_block_number(api_key, start_timestamp)
   end_block = fetch_block_number(api_key, end_timestamp)


   print(f"Start Block: {start_block}")
   print(f"End Block: {end_block}")


   # Fetch the total number of transactions within the block range
   transactions_by_day = fetch_total_transactions(api_key, start_block, end_block)


   # Convert the dictionary to a DataFrame for plotting
   df = pd.DataFrame(list(transactions_by_day.items()), columns=['Date', 'TransactionCount'])
   df['Date'] = pd.to_datetime(df['Date'])
   df.set_index('Date', inplace=True)
  
   # Plot the number of transactions per day as a line plot
   df.plot(kind='line', title='Number of Transactions Per Day in January 2024')
   plt.xlabel('Date')
   plt.ylabel('Number of Transactions')
   plt.grid(True)
   plt.show()


if __name__ == "__main__":
   main()

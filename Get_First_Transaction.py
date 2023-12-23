import requests
from datetime import datetime

def get_first_transaction(wallet_address):
    # Construct the URL for getting transaction history for the specified address
    url = f'https://btcscan.org/api/address/{wallet_address}/txs/chain'

    # Make the GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        transactions = response.json()

        # Check if there are any transactions
        if transactions:
            # Retrieve information about the first transaction
            first_transaction = transactions[0]
            return first_transaction
        else:
            return None
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_date_from_block_time(block_time):
    # Convert block time (Unix timestamp) to a human-readable date
    return datetime.utcfromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S UTC')

def process_addresses(input_file, output_file):
    with open(input_file, 'r') as f:
        addresses = f.read().splitlines()

    for wallet_address in addresses:
        first_transaction_info = get_first_transaction(wallet_address)

        # Write the information to the output file in real-time
        with open(output_file, 'a') as output:
            output.write(f"{wallet_address}\n")
            if first_transaction_info:
                output.write(f"{get_date_from_block_time(first_transaction_info['status']['block_time'])}\n\n")
            else:
                output.write("No transactions found for the specified wallet.\n")

            # Flush the output buffer to write to the file in real-time
            output.flush()

if __name__ == "__main__":
    
    process_addresses('List_of_wallets.txt', 'Output_BTC_TX_Date.txt')

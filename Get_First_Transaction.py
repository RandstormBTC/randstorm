import requests

def get_first_transaction_info(api_key, address, output_file):
    api_url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}/full?limit=1&token={api_key}'

    try:
        response = requests.get(api_url)
        data = response.json()

        # Check if the request was successful (status code 200)
        if response.status_code == 200 and 'txs' in data and data['txs']:
            transaction = data['txs'][0]
            output = f"Address: {address}\n"
            output += f"First Transaction: {transaction.get('received', 'N/A')}\n"

            # Display current balance in BTC
            current_balance_satoshis = data['balance']
            current_balance_btc = current_balance_satoshis / 100000000  # Convert satoshis to BTC
            output += f"Current Balance: {current_balance_btc} BTC\n\n"

            with open(output_file, 'a') as file:
                file.write(output)
                print(f"Output for {address} written to {output_file}")
        else:
            print(f"No transactions found for the given address: {address}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def process_addresses(api_key, addresses_file, output_file):
    try:
        with open(addresses_file, 'r') as file:
            addresses = file.read().splitlines()

        for address in addresses:
            get_first_transaction_info(api_key, address, output_file)

    except FileNotFoundError:
        print(f"Error: The file '{addresses_file}' was not found.")

# Replace 'your_addresses.txt', 'your_output.txt', and 'your_api_key_here' with the actual file paths and API key you want to use
addresses_file_path = 'addresses_file_path.txt'
output_file_path = 'output_file_path.txt'
api_key = 'api_key'
process_addresses(api_key, addresses_file_path, output_file_path)

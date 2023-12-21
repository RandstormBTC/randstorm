import coincurve
import hashlib
import bech32
import base58
import time
import os
import random
import multiprocessing
import sys
import mmap
from Crypto.Hash import SHA256, RIPEMD160
from rich.console import Console
console = Console()
# =========================================================================================
btc = '''

██████╗░░█████╗░███╗░░██╗██████╗░░██████╗████████╗░█████╗░██████╗░███╗░░░███╗
██╔══██╗██╔══██╗████╗░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗░████║
██████╔╝███████║██╔██╗██║██║░░██║╚█████╗░░░░██║░░░██║░░██║██████╔╝██╔████╔██║
██╔══██╗██╔══██║██║╚████║██║░░██║░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██║╚██╔╝██║
██║░░██║██║░░██║██║░╚███║██████╔╝██████╔╝░░░██║░░░╚█████╔╝██║░░██║██║░╚═╝░██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝
'''
# ============================================================================================
console.print(btc)

class MathRandomSimulator:
    def __init__(self, psize=32, start_timestamp=1262304000, end_timestamp=1388534399):
        # Initialize the random number generator pool and set the initial state
        self.rng_pool = bytearray()
        self.rng_pptr = 0  # Pointer to the current position in the pool
        self.rng_psize = psize  # Size of the pool

        # Generate a random seed within the specified time range (2010 - 2014) using Unix timestamps
        self._seed = random.randint(start_timestamp, end_timestamp)
        random.seed(self._seed)

    @property
    def seed(self):
        # Get the current seed value used by the random number generator
        return self._seed

    def rng_get_bytes(self, size):
        # Generate and retrieve the next 'size' bytes from the random number generator pool
        while len(self.rng_pool) < size:
            random_value = int(random.random() * (2**32))
            self.rng_pool.extend(random_value.to_bytes(4, 'big'))

        result = bytes(self.rng_pool[:size])
        self.rng_pool = self.rng_pool[size:]  # Remove the bytes that were returned
        return result

def custom_private_key_generator(rng_simulator=None):
    # If no random number generator simulator is provided, create a new one
    rng = MathRandomSimulator()

    # Generate 32 bytes (256 bits) as the private key
    private_key_bytes = rng.rng_get_bytes(32)

    # Convert the bytes to a hexadecimal string
    private_key_hex = private_key_bytes.hex()

    # Return the generated private key in hexadecimal format
    return private_key_hex
    
def generate_compressed_P2P_address(private_key):
    # Convert the private key from hexadecimal string to bytes
    private_key_bytes = bytes.fromhex(private_key)

    # Derive the compressed public key from the private key using the coincurve library
    public_key = coincurve.PrivateKey(private_key_bytes).public_key.format(compressed=True)

    # Calculate the RIPEMD160 hash of the SHA256 hash of the compressed public key
    public_key_hash = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).hexdigest()

    # Prepend '00' to the public key hash to create the extended public key hash
    extended_public_key_hash = '00' + public_key_hash

    # Calculate the checksum using double SHA256 on the extended public key hash
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(extended_public_key_hash)).digest()).hexdigest()[:8]

    # Concatenate the extended public key hash and the checksum, then encode in base58
    p2pkh_address = base58.b58encode(bytes.fromhex(extended_public_key_hash + checksum))

    # Return the compressed P2PKH address as a string
    return p2pkh_address.decode()
    
total_keys_generated = multiprocessing.Value('i', 0)

def search_for_match(database, address_set, process_id, result_queue, rng_simulator, mmapped_file):
    global total_keys_generated  # Use the shared variable for keys/sec

    iteration = 0
    keys_generated_at_start = total_keys_generated.value
    start_time = time.time()

    while True:
        # Generate Private HEX and public Key
        private_key = custom_private_key_generator(rng_simulator)
        
        # Generate the compressed P2PKH Bitcoin address using the private key
        compressed_p2pkh_address = generate_compressed_P2P_address(private_key)

        # Increment the total count
        with total_keys_generated.get_lock():
            total_keys_generated.value += 1

        # Print every 10,000 keys
        if iteration % 10000 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time

            keys_generated = total_keys_generated.value - keys_generated_at_start
            keys_per_second = keys_generated / elapsed_time if elapsed_time > 0 else 0

            print(f"\rGenerated Keys: \033[92m{total_keys_generated.value:,.0f}\033[0m"
                  f" | Keys/Second: \033[92m{keys_per_second:,.0f}\033[0m", end='', flush=True)
            
            # Search for a match in the memory-mapped file
            if compressed_p2pkh_address in mmapped_file:
                result_queue.put({
                    'private_key_hex': private_key,
                    'address_info': compressed_p2pkh_address,
                })
                break

        iteration += 1  # Increment the iteration counter

if __name__ == '__main__':

    # Define the file path for the memory-mapped file containing Bitcoin addresses
    file_path = '40,000 dormant bitcoin addresses.txt'

    # Initialize the address_set
    address_set = set()

    # Read the entire file into a list of lines
    with open(file_path, 'rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            num_lines = 0
            while True:
                line = mmapped_file.readline()
                if not line:
                    break
                num_lines += 1
                address_set.add(line.strip()) 
            print(f"Opening {file_path} - \033[92m{num_lines:,.0f}\033[0m Addresses")

    # Initialize the database and multiprocessing
    database = set()
    processes = []
    result_queue = multiprocessing.Queue()
    rng_simulator = MathRandomSimulator()

    try:
        # Create and start processes for searching matches in parallel
        for cpu in range(multiprocessing.cpu_count()):
            process = multiprocessing.Process(target=search_for_match, args=(database, address_set, cpu, result_queue, rng_simulator, file_path))
            processes.append(process)
            process.start()

        # Keep the main process running while the child processes execute
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt to terminate processes gracefully
        print("\nReceived KeyboardInterrupt. Terminating processes.")
        
        # Terminate and join each process
        for process in processes:
            process.terminate()
            process.join()

        # Process and write results to a file
        while not result_queue.empty():
            result = result_queue.get()
            with open('winner.txt', 'a') as output_file:
                output_file.write(f"HEX: {result['private_key_hex']}\n")
                output_file.write(f"P2SH Bitcoin Address: {result['p2sh_p2wpkh_address']}\n")

        print("\nAll processes finished.")
        sys.exit(0)

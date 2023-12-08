import coincurve
import hashlib
import bech32
import base58
import time
import os
from Crypto.Hash import SHA256, RIPEMD160
import random
import multiprocessing
import sys
import mmap
from rich.console import Console
console = Console()
# =========================================================================================
btc = '''

    ██████╗░██╗████████╗░█████╗░░█████╗░██╗███╗░░██╗
    ██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗██║████╗░██║
    ██████╦╝██║░░░██║░░░██║░░╚═╝██║░░██║██║██╔██╗██║
    ██╔══██╗██║░░░██║░░░██║░░██╗██║░░██║██║██║╚████║
    ██████╦╝██║░░░██║░░░╚█████╔╝╚█████╔╝██║██║░╚███║
    ╚═════╝░╚═╝░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝

    ░█▀█░▀▀▄░█▀█░░░█▀▀░█▀▀░█▀█░█▀▄░█▀▀░█░█
    ░█▀▀░▄▀░░█▀▀░░░▀▀█░█▀▀░█▀█░█▀▄░█░░░█▀█
    ░▀░░░▀▀▀░▀░░░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
'''
# ============================================================================================
console.print(btc)

class MathRandomSimulator:
    # Equivalent to SecureRandom() used in JSBN javascript library with Math.random()
    def __init__(self, psize=32):
        self.rng_pool = bytearray()
        self.rng_pptr = 0
        self.rng_psize = psize
        
        while len(self.rng_pool) < self.rng_psize:
            t = int(random.random() * 65536) 
            self.rng_pool.extend(t.to_bytes(2, 'big'))

        self.rng_pptr = 0

    def next_bytes(self, size):
        return self.rng_get_bytes(size)

    def rng_get_bytes(self, size):
        result = bytes(self.rng_pool[self.rng_pptr:self.rng_pptr + size])
        self.rng_pptr += size
        return result
        
def custom_private_key_generator(rng_simulator=None):
    # If no RNG simulator is provided, create a new MathRandomSimulator instance
    rng_simulator = MathRandomSimulator()

    # Get the next 32 bytes from the RNG simulator as private key bytes
    private_key_bytes = rng_simulator.next_bytes(32)

    # Convert the private key bytes to a hexadecimal string
    private_key_hex = private_key_bytes.hex()

    # Return the generated private key as a hexadecimal string
    return private_key_hex
    
def generate_P2P_address(private_key):  #Speed: 12,000 addresses per second.
    private_key_bytes = bytes.fromhex(private_key)
    public_key = coincurve.PrivateKey(private_key_bytes).public_key.format(compressed=False)
    public_key_hash = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).hexdigest()
    extended_public_key_hash = '00' + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(extended_public_key_hash)).digest()).hexdigest()[:8]
    p2pkh_address = base58.b58encode(bytes.fromhex(extended_public_key_hash + checksum))
    return p2pkh_address.decode()

# Shared variable to store total count
total_keys_generated = multiprocessing.Value('i', 0)

def search_for_match(database, address_set, process_id, result_queue, rng_simulator, file_path):
    global total_keys_generated  # Use the shared variable

    # Open the file using mmap
    with open(file_path, 'rb') as file:
        with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            iteration = 0
            while True:
                # Generate Private HEX and P2P public Key
                private_key = custom_private_key_generator(rng_simulator)
                p2p_address = generate_P2P_address(private_key)

                # Increment the total count
                with total_keys_generated.get_lock():
                    total_keys_generated.value += 1

                # Check if it's time to print every 10,000 keys
                if iteration % 100000 == 0:
                    print(f"\rTotal Generated Keys: \033[92m{total_keys_generated.value:,.0f}\033[0m", end='', flush=True)

                if 'p2pkh_address.decode()' in p2p_address and p2p_address in mmapped_file:
                    result_queue.put({
                        'private_key_hex': private_key,
                        'address_info': p2p_address,
                    })
                    break  # exit the loop when a match is found

                iteration += 1  # Increment the iteration counter

if __name__ == '__main__':

    file_path = 'P2P_addresses_December_06_2023.txt'
    
    # Read the entire file into a list of lines
    with open(file_path, 'r') as file:
        address_list = file.readlines()

    num_lines = len(address_list)
    print(f"Opening {file_path} - {num_lines:,.0f} Addresses")

    # Process the lines as needed
    address_set = set(line.strip() for line in address_list)

    database = set()  # Initialize the database here

    processes = []
    result_queue = multiprocessing.Queue()
    rng_simulator = MathRandomSimulator()

    try:
        for cpu in range(multiprocessing.cpu_count()):
            process = multiprocessing.Process(target=search_for_match, args=(database, address_set, cpu, result_queue, rng_simulator, file_path))
            processes.append(process)
            process.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt. Terminating processes.")
        for process in processes:
            process.terminate()
            process.join()

        while not result_queue.empty():
            result = result_queue.get()
            with open('winner.txt', 'a') as output_file:
                output_file.write(f"HEX: {result['private_key_hex']}\n")
                output_file.write(f"P2SH Bitcoin Address: {result['p2sh_p2wpkh_address']}\n")

        print("\nAll processes finished.")
        sys.exit(0)

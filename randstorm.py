import random
import time
from multiprocessing import Pool
import coincurve
import hashlib
import base58
from rich.console import Console
console = Console()
# =========================================================================================
Randstorm = '''

██████╗░░█████╗░███╗░░██╗██████╗░░██████╗████████╗░█████╗░██████╗░███╗░░░███╗
██╔══██╗██╔══██╗████╗░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗░████║
██████╔╝███████║██╔██╗██║██║░░██║╚█████╗░░░░██║░░░██║░░██║██████╔╝██╔████╔██║
██╔══██╗██╔══██║██║╚████║██║░░██║░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██║╚██╔╝██║
██║░░██║██║░░██║██║░╚███║██████╔╝██████╔╝░░░██║░░░╚█████╔╝██║░░██║██║░╚═╝░██║
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝
'''
# =========================================================================================
console.print(Randstorm)

class SecureRandom:
    def __init__(self, seed):
        self.rng_state = None
        self.rng_pool = []
        self.rng_pptr = 0
        self.rng_psize = 32
        random.seed(seed)
        for _ in range(self.rng_psize):
            self.rng_pool.append(random.randint(0, 255))
        self.rng_pptr = 0

    def rng_get_byte(self):
        if self.rng_pptr >= len(self.rng_pool):
            self.rng_pptr = 0
            self.rng_pool = [random.randint(0, 255) for _ in range(self.rng_psize)]
        byte = self.rng_pool[self.rng_pptr]
        self.rng_pptr += 1
        return byte

    def rng_get_bytes(self, length):
        result = bytearray(length)
        for i in range(length):
            result[i] = self.rng_get_byte()
        return result
def custom_private_key_generator(rng_simulator=None):
    # If no random number generator simulator is provided, create a new one
    rng = SecureRandom()

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

def generate_hex(seed):
    # Set the total number of keys to generate, adjust as needed
    hex_keys = 145000000  # 145 million keys for 1 day
    current_seed = seed

    # Create a secure random number generator
    secure_rng = SecureRandom(current_seed)

    for i in range(hex_keys):
        # Generate a random private key in hexadecimal format
        random_bytes = secure_rng.rng_get_bytes(32)
        hex_representation = random_bytes.hex()
        private_key = hex_representation

        # Generate the compressed P2PKH address from the private key
        p2pkh_address = generate_compressed_P2P_address(private_key)

        # Check if the generated address matches
        if p2pkh_address == target_address:
            print(f"Match found!\nPrivate Key: {private_key}")

            # Append the matched private key to a file
            with open("matched_private_keys.txt", "a") as file:
                file.write(f"{private_key}\n")

        current_seed += 1
        
        # Display progress every 10,000 keys
        if i % 10000 == 0:
            end_time = time.time()
            elapsed_time = end_time - start_time
            addresses_per_second = (i + 1) / elapsed_time

            # Print the progress in a single line with color-coded information
            print(f"\rGenerated \033[93m{i}\033[0m Keys | Speed: \033[93m{addresses_per_second:.2f} Keys/s\033[0m | Current Seed: \033[93m{current_seed}\033[0m", end='', flush=True)

if __name__ == '__main__':
    # Set the number of parallel processes (cores) to use
    num_processes = 6
    
    target_address = "1NUhcfvRthmvrHf1PAJKe5uEzBGK44ASBD"

    # Display the target address at the beginning
    print(f"Searching for: \033[93m{target_address}\033[0m\n")

    start_time = time.time()

    # Use multiprocessing.Pool to parallelize the generation of random keys
    with Pool(num_processes) as pool:
        # Define the range of seeds for each process, March 1, 2014 = 1393635661000
        seeds = range(1393635661000, 1393635661000 + num_processes)

        # Map the generate_hex function to the pool of processes
        pool.map(generate_hex, seeds)

    # Record the end time and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 1.4 Billion seeds. Change as needed. 
    hex_keys = 1400000000 * num_processes 
    addresses_per_second = hex_keys / elapsed_time

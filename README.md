# Randstorm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
From 2011 - 2015 many popular crypto exchanges used BitcoinJS to generate private keys. 

For an incredibly popular library, there was an issue in BitcoinJS:

“The most common variations of the library attempts to collect entropy
from window.crypto's CSPRNG, but due to a type error in a comparison
this function is silently stepped over without failing. Entropy is
subsequently gathered from math.Random (a 48bit linear congruential
generator, seeded by the time in some browsers), and a single
execution of a medium resolution timer. In some known configurations
this system has substantially less than 48 bits of entropy.”

This program generates a Random Private Key using the python equivalent to SecureRandom() in JSBN javascript library with Math.random(). 

![Project Image](SecureRandom.png)

Rather than using the more secure libraries to generate private keys, this private key generator function emulates the weak private key generation used in the JSBN library from 2011 - 2015:

```python
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
```

Rather than using the more secure libraries to generate private keys, this function class MathRandomSimulator emulates the weak private key generation used in the JSBN library. 

Then a P2P Bitcoin address is creates using this private key.

<pre>
```
p2p address:
1FaVN8XPyNHchgkNRZMwBQGqTMf531yebX
```
</pre>

```python
def generate_P2P_address(private_key):  #Speed: 12,000 addresses per second.
    private_key_bytes = bytes.fromhex(private_key)
    public_key = coincurve.PrivateKey(private_key_bytes).public_key.format(compressed=False)
    public_key_hash = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).hexdigest()
    extended_public_key_hash = '00' + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(extended_public_key_hash)).digest()).hexdigest()[:8]
    p2pkh_address = base58.b58encode(bytes.fromhex(extended_public_key_hash + checksum))
    return p2pkh_address.decode()
```

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

Provide step-by-step instructions on how to install your project. You can include code snippets or commands if necessary.

```bash
npm install

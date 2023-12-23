![Project Image](RandstormProgram.png)

From 2011 - 2015 many popular crypto exchanges used BitcoinJS to generate private keys. There was an issue with BitcoinJS due to the absence of `window.crypto.random` in many browsers. Consequently, this led to entropy being gathered from `Math.random()`. Using Math.random() for cryptographic key generation should never be done. However, during the 2011-2015 timeframe it was used on all major browsers to generate private keys.

![Project Image](SecureRandomFunction.png)

This means that the Private Key is generated using rng_seed_time() as the only source of entropy. If the address was generated on December 24, 0201, 2:44:56 AM, then using the [Unix epoch time](https://www.epochconverter.com/) we can see that the seed = 55793394904000. This is the Unix epoch time in milliseconds. Then using SecureRandom() with the seed to generate the address, we can retrieve the private key.

## Seed Generation

Since we can't determine when the address was generated, we can examine when the first transaction took place using the blockchain, using an API call from a website such as blockcypher.com:

*Address: 1NUhcfvRthmvrHf1PAJKe5uEzBGK44ASBD
First Transaction: 2014-03-17T07:41:22Z
Current Balance: 1.9999 BTC*

Convert the date 2014-03-17T07:41:22Z to Unix epoch time in milliseconds: 1395042082000

Now, get the date from whatever time period you want to try before March 3, 2014.

March 1, 2014 = 1393635661000

1395042082000 - 1393635661000 = 1.4 Billion Seeds

## Key Generating and Searching Speed

Using the implementation of SecureRandom(), set the seed to March 1, 2014 = 1393635661000 and generate keys incrementally until the date of the first transaction:

Seed: 1310691661000 Hex: 6ad2d763712eae6428e2922d7181f92fb70d0e564d1dd38dd0aa9b34b844c0cb P2PKH: 1JbryLqejpB17zLDNspRyJwjL5rjXW7gyw
Seed: 1310691661001 Hex: fb6ad847a48da87b332b565b548347078a1b9890b9c352a4d9993ae09c189fa6 P2PKH: 1273EG6iByUWoDY8PrCBEhJsEBLEzk1rEi
Seed: 1310691661002 Hex: 126a2214040a5e6ef26902b4f6a964af4b82b6ef537e09ea1d2b936dab5af571 P2PKH: 1MyrpGdKhu3ASwU6GWdEGKX3mocWVnVXYV
Seed: 1310691661003 Hex: b2a6694fbb85a9f199bdfb1599242f12d64b036f56b552d92ac1bfe7b2caf55b P2PKH: 1PuGm9G5JQTxy4XrB2gSwuHGoG3Wv5YtaC
Seed: 1310691661004 Hex: cb33e1431ad31a2adf9bbc545539a852e3756d5019db617422d18d86b241e8a1 P2PKH: 1H8uFkvWfs4bsy9AkRFy8nhS6bBm1ntkqh
Seed: 1310691661005 Hex: 691064ed9ea535b84637b34b32e73344464335147847cb6cc9efe573af2cfe10 P2PKH: 1CXE4mTtW1Pk8xqceHxgzyZq3uWCDJCfRz
Seed: 1310691661006 Hex: 7299f801c3957e33864f3b0f0183bf372792cdae8b8b468fb351d4e6e73fb691 P2PKH: 1GxXoWf2NhG3xrmtMSmWy3cPxvhfULMMAR
Seed: 1310691661007 Hex: eca44bb50206e39b10d8980332d1fe8ecc994bb87752475f1beba6fc71a030c6 P2PKH: 1DLwkoxdUUPeF8c1hWiLYtkj8DTb7mFUYi
Seed: 1310691661008 Hex: e7ce76437e0a836626b2c6288c608bd8ad803311615d122679fb86d4bba92684 P2PKH: 1FqxzCTL4pRJFUXSxZmefNzevjhvmT5i3n
Seed: 1310691661009 Hex: ac4a70b3482e19e8acf12d733ee518cc375de32900b3978f88f3ca8def46c170 P2PKH: 1Emb22aih1sP5T55R8AaMJGMDz7rs1117C
Seed: 1310691661010 Hex: ef212bcf506aff742882c25c1a573565165a437f797c617a841ed8399f54f108 P2PKH: 1GsJqM7dZ5BqvhyKuaTK3X9zb6smpD3pdu

...


## Download & Installing

```bash
git clone https://github.com/RandstormBTC/randstorm/
cd randstorm
pip install -r requirements.txt
```

Run On Windows (cmd / powershell):
```bash
python randstorm.py
```
Run On Linux (debian):
```bash
python3 randstorm.py
```
## Download Addressess 
You can implement a function to generate Addressess and check the Balance if you want to spend $10,000 in API calls... 

Here is a good list: 

[42,000 dormant bitcoin addresses](https://steemit.com/dormant/@rogerripple/42-000-dormant-bitcoin-addresses)

Or you can find an updated List of all funded Bitcoin addresses at:

http://addresses.loyce.club/

To save all P2P addressess to a file use:
<pre>
grep '^1' Bitcoin_addresses_December_06_2023.txt 
</pre>

Update the file_path in randstorm.py 

## Disclaimer
This software is for education purporses only and should not be configured and used to find (Bitcoin/Altcoin) address hash (RIPEMD-160) collisions and use (steal) credit from third-party (Bitcoin/Altcoin) addresses. This mode might be allowed to recover lost private keys of your own public addresses only.

Another mostly legal use case is a check if the (Bitcoin/Altcoin) addresses hash (RIPEMD-160) is already in use to prevent yourself from a known hash (RIPEMD-160) collision and double use. Some configurations are not allowed in some countries.

## Sources:

 <https://www.unciphered.com/blog/randstorm-you-cant-patch-a-house-of-cards>

 <https://jandemooij.nl/blog/math-random-and-32-bit-precision/>

 <https://medium.com/@betable/tifu-by-using-math-random-f1c308c4fd9d>

## Donate:
BTC: bc1q2rqz0mzwxdm0umhlllsyd5rt30uh8kswhqcnqp

// SecureRandom() function which uses Math.Random to generte a 32 byte Hex string and provides detailed output for each state of the RNG. 
// Run it like this: node SecureRandomDebug.js > output.txt

function SecureRandom3() {
    var SEED_TIME_VALUE = 1294200190000;
    this.pool = null;
    this.pptr = 0;
    this.poolSize = 256;
    this.state = null;  // Added to avoid 'undefined' errors

this.seedInt = function (x) {
    console.log("SeedInt input:", x);

    this.pool[this.pptr++] ^= x & 255;
    console.log("After XORing low byte:", this.pool);

    this.pool[this.pptr++] ^= (x >> 8) & 255;
    console.log("After XORing second byte:", this.pool);

    this.pool[this.pptr++] ^= (x >> 16) & 255;
    console.log("After XORing third byte:", this.pool);

    this.pool[this.pptr++] ^= (x >> 24) & 255;
    console.log("After XORing fourth byte:", this.pool);

    if (this.pptr >= this.poolSize) {
        this.pptr -= this.poolSize;
        console.log("Ptr wrapped around. New value:", this.pptr);
    }
};
    this.seedTime = function () {
        this.seedInt(SEED_TIME_VALUE);
    };

this.getByte = function () {
    if (this.state == null) {
        console.log("Initializing PRNG state...");

        console.log("Seeding time...");
        this.seedTime();
        console.log("Time seeded.");

        this.state = this.ArcFour();
        console.log("ArcFour PRNG state created.");

        // Debug output for the entire pool
        console.log("Current Pool:", this.pool);

        // Initializing PRNG state with the current pool
        this.state.init(this.pool);
        console.log("PRNG state initialized.");

        // Reset pool for security
        for (this.pptr = 0; this.pptr < this.pool.length; ++this.pptr)
            this.pool[this.pptr] = 0;
        this.pptr = 0;

        console.log("Pool reset.");
    }

// Generating a random byte using the PRNG
var randomByte = this.state.next();

// Debug output in "Decimal -> Hex" format
console.log("Decimal -> Hex:", randomByte, "->", randomByte.toString(16));

return randomByte;
    };

    // Initialize the pool
    if (this.pool == null) {
        this.pool = new Array(this.poolSize);
        this.pptr = 0;
        var t;

        // Fill the pool with random values
var counter = 1;
var byteOutput = "";

console.log("Random 16-bit Value: | High Byte | Low Byte |");

while (this.pptr < this.poolSize) {
    t = Math.floor(65536 * Math.random());

    // Debugging output for Math.random() values
    console.log("Byte " + counter + ": " + t + "   " + (t & 255) + "   " + (t >>> 8));

    // Extract and output the high byte
    this.pool[this.pptr++] = t & 255;
    counter++;

    // Extract and output the low byte
    this.pool[this.pptr++] = t >>> 8;
    counter++;
}

// Display the collected byte information on a single line
console.log(byteOutput);
        this.pptr = 0;
        this.seedTime();
    }
}

SecureRandom3.prototype.ArcFour = function () {
    function ArcFour() {
        this.i = 0;
        this.j = 0;
        this.S = new Array(256);
    }

    function ARC4init(key) {
        var i, j, t;
        for (i = 0; i < 256; ++i)
            this.S[i] = i;

        // Debug output for the initial state of S
        console.log("Initial State of S:", this.S);

        j = 0;
        for (i = 0; i < 256; ++i) {
            j = (j + this.S[i] + key[i % key.length]) & 255;
            t = this.S[i];
            this.S[i] = this.S[j];
            this.S[j] = t;
        }

        // Debug output for the final state of S after initialization
        console.log("Final State of S after Initialization:", this.S);

        this.i = 0;
        this.j = 0;
    }

function ARC4next() {
    var t;
    this.i = (this.i + 1) & 255;
    this.j = (this.j + this.S[this.i]) & 255;
    t = this.S[this.i];
    this.S[this.i] = this.S[this.j];
    this.S[this.j] = t;

    // Debug output for the values used in each next() step
    console.log("i:", this.i, "j:", this.j, "t:", t);

    return this.S[(t + this.S[this.i]) & 255];
}

    ArcFour.prototype.init = ARC4init;
    ArcFour.prototype.next = ARC4next;

    return new ArcFour();
};

// SecureRandom3
var random3 = new SecureRandom3();
var privateKeyBytes3 = new Uint8Array(32);
for (var k = 0; k < privateKeyBytes3.length; k++) {
    privateKeyBytes3[k] = random3.getByte();
}
var privateKeyHex3 = Array.from(privateKeyBytes3).map(b => ('0' + b.toString(16)).slice(-2)).join('');

console.log('32 Byte Hex String:', privateKeyHex3);

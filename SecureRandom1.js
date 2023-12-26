// Generates a private key based on Math.random() with 2 slightly different implementations. 

function SecureRandom3() {
var SEED_TIME_VALUE = 1294200190000;
    this.pool = null;
    this.pptr = 0;
    this.poolSize = 256;

    this.seedTime = function () {
        this.seedInt(SEED_TIME_VALUE);
    };

    this.seedInt = function (x) {
        this.pool[this.pptr++] ^= x & 255;
        this.pool[this.pptr++] ^= (x >> 8) & 255;
        this.pool[this.pptr++] ^= (x >> 16) & 255;
        this.pool[this.pptr++] ^= (x >> 24) & 255;
        if (this.pptr >= this.poolSize) this.pptr -= this.poolSize;
    };
	
    this.getByte = function () {
        if (this.state == null) {
            this.seedTime();
            this.state = this.ArcFour();
            this.state.init(this.pool);
            for (this.pptr = 0; this.pptr < this.pool.length; ++this.pptr)
                this.pool[this.pptr] = 0;
            this.pptr = 0;
        }

        return this.state.next();
    };

    // Initialize the pool with junk if needed.
    if (this.pool == null) {
        this.pool = new Array(this.poolSize);
        this.pptr = 0;
        var t;

        while (this.pptr < this.poolSize) {
            t = Math.floor(65536 * Math.random());
            this.pool[this.pptr++] = t >>> 8;
            this.pool[this.pptr++] = t & 255;
        }
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
        j = 0;
        for (i = 0; i < 256; ++i) {
            j = (j + this.S[i] + key[i % key.length]) & 255;
            t = this.S[i];
            this.S[i] = this.S[j];
            this.S[j] = t;
        }
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
        return this.S[(t + this.S[this.i]) & 255];
    }

    ArcFour.prototype.init = ARC4init;
    ArcFour.prototype.next = ARC4next;

    return new ArcFour();
};

var SecureRandom2 = function () {
var SEED_TIME_VALUE = 1294200190000;

    this.pool;
    this.pptr;
    this.poolSize = 256;
	this.state;

    // Mix in the fixed value (1294200190000) as the "current time"
    this.seedTime = function () {
        this.seedInt(SEED_TIME_VALUE);
    };

    this.seedInt = function (x) {
        this.pool[this.pptr++] ^= x & 255;
        this.pool[this.pptr++] ^= (x >> 8) & 255;
        this.pool[this.pptr++] ^= (x >> 16) & 255;
        this.pool[this.pptr++] ^= (x >> 24) & 255;
        if (this.pptr >= this.poolSize) this.pptr -= this.poolSize;
    };

    // Arcfour is a PRNG
    this.ArcFour = function () {
        function Arcfour() {
            this.i = 0;
            this.j = 0;
            this.S = new Array();
        }

        // Initialize arcfour context from key, an array of ints, each from [0..255]
        function ARC4init(key) {
            var i, j, t;
            for (i = 0; i < 256; ++i)
                this.S[i] = i;
            j = 0;
            for (i = 0; i < 256; ++i) {
                j = (j + this.S[i] + key[i % key.length]) & 255;
                t = this.S[i];
                this.S[i] = this.S[j];
                this.S[j] = t;
            }
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
            return this.S[(t + this.S[this.i]) & 255];
        }

        Arcfour.prototype.init = ARC4init;
        Arcfour.prototype.next = ARC4next;

        return new Arcfour();
    };

    // Initialize the pool with junk if needed.
    if (this.pool == null) {
        this.pool = new Array();
        this.pptr = 0;
        var t;

        while (this.pptr < this.poolSize) {
            t = Math.floor(65536 * Math.random());
            this.pool[this.pptr++] = t >>> 8;
            this.pool[this.pptr++] = t & 255;
        }
        this.pptr = 0;
    }
};


// SecureRandom3
var random3 = new SecureRandom3();
var privateKeyBytes3 = new Uint8Array(32);
for (var k = 0; k < privateKeyBytes3.length; k++) {
    privateKeyBytes3[k] = random3.getByte();
}
var privateKeyHex3 = Array.from(privateKeyBytes3).map(b => ('0' + b.toString(16)).slice(-2)).join('');

console.log('SecureRandom1:', privateKeyHex3);

// SecureRandom2
var random2 = new SecureRandom2();
var privateKeyBytes2 = new Uint8Array(32);
for (var j = 0; j < privateKeyBytes2.length; j++) {
    privateKeyBytes2[j] = random2.pool[j];
}
var privateKeyHex2 = Array.from(privateKeyBytes2).map(b => ('0' + b.toString(16)).slice(-2)).join('');

console.log('SecureRandom2:', privateKeyHex2);

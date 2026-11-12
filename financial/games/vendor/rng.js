/* Mr. K's Classroom Worksheet Generator — seeded random numbers.
   Everything random goes through this so a worksheet can be reproduced from its seed. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});

  function hash(str) {                       // string -> 32-bit unsigned int (FNV-1a)
    var h = 2166136261 >>> 0;
    str = String(str);
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h >>> 0;
  }

  function RNG(seed) {
    this.state = (typeof seed === 'number' ? seed : hash(seed)) >>> 0;
  }
  RNG.prototype.next = function () {          // mulberry32
    var a = (this.state = (this.state + 0x6D2B79F5) | 0);
    var t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  RNG.prototype.int = function (lo, hi) {     // inclusive both ends
    if (hi < lo) { throw new Error('rng.int: empty range ' + lo + '..' + hi); }
    return lo + Math.floor(this.next() * (hi - lo + 1));
  };
  RNG.prototype.nonzero = function (lo, hi) { // integer in [lo,hi] excluding 0
    var v; do { v = this.int(lo, hi); } while (v === 0); return v;
  };
  RNG.prototype.chance = function (p) { return this.next() < p; };
  RNG.prototype.sign = function () { return this.next() < 0.5 ? -1 : 1; };
  RNG.prototype.pick = function (arr) { return arr[Math.floor(this.next() * arr.length)]; };
  RNG.prototype.shuffle = function (arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(this.next() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  };
  RNG.prototype.fork = function (label) { return new RNG(hash(this.state + '|' + label)); };

  NS.rng = { RNG: RNG, hash: hash, make: function (seed) { return new RNG(seed); } };
})(typeof window !== 'undefined' ? window : globalThis);


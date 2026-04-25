import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {encode, decode} from "../src/base91x.js";
import {webcrypto as crypto} from "node:crypto";

function hexToBytes(hex) {
    if (hex.length === 0) return new Uint8Array();
    return Uint8Array.from(hex.match(/.{1,2}/g).map(b => parseInt(b, 16)));
}

function bytesToHex(bytes) {
    return Array.from(bytes)
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");
}

const vectors = JSON.parse(
    readFileSync(new URL("./test.json", import.meta.url))
);

// fixed tests cross validation

for (const [hex, expected] of Object.entries(vectors)) {
    test(`encode ${hex}`, () => {
        const input = hexToBytes(hex);
        assert.equal(encode(input), expected);
    });

    test(`decode ${expected}`, () => {
        const output = decode(expected);
        assert.equal(bytesToHex(output), hex);
    });
}

// random roundtrip

function randomBytes(len) {
    const arr = new Uint8Array(len);
    crypto.getRandomValues(arr);
    return arr;
}

test("random roundtrip", () => {
    for (let i = 0; i < 100; i++) {
        const input = randomBytes((Math.random() * 100) | 0);
        const encoded = encode(input);
        const decoded = decode(encoded);

        assert.deepEqual(decoded, input);
    }
});
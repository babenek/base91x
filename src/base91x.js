/*
MIT License

Copyright (c) 2026 Roman Babenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

const BASE91X_LEN = 91;
const CHAR_BIT = 8;
const B91WORD_BIT = 13;
const B91WORD_MASK = 0x1FFF;

const BASE91X_ALPHABET = [
    '!', '~', '}', '|', '{', 'z', 'y', 'x', 'w', 'v',
    'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l',
    'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b',
    'a', '`', '_', '^', ']', '#', '[', 'Z', 'Y', 'X',
    'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N',
    'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D',
    'C', 'B', 'A', '@', '?', '>', '=', '<', ';', ':',
    '9', '8', '7', '6', '5', '4', '3', '2', '1', '0',
    '/', '.', '-', ',', '+', '*', ')', '(', '$', '&',
    '%'
];

const BASE91X_ZYX = new Int16Array([
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, +0, -1, 35, 88, 90, 89, -1, 87, 86, 85, 84, 83, 82, 81, 80,
    79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64,
    63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48,
    47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, -1, 34, 33, 32,
    31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
    15, 14, 13, 12, 11, 10, +9, +8, +7, +6, +5, +4, +3, +2, +1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
]);


export function encode(input) {
    let collector = 0;
    let bitCollected = 0;

    const out = [];

    for (let i = 0; i < input.length; i++) {
        collector |= input[i] << bitCollected;
        bitCollected += CHAR_BIT;

        while (bitCollected >= B91WORD_BIT) {
            const value = collector & B91WORD_MASK;

            const quot = (value / BASE91X_LEN) | 0;
            const rem = value - quot * BASE91X_LEN;

            out.push(BASE91X_ALPHABET[rem]);
            out.push(BASE91X_ALPHABET[quot]);

            collector >>= B91WORD_BIT;
            bitCollected -= B91WORD_BIT;
        }
    }

    if (bitCollected !== 0) {
        const value = collector & B91WORD_MASK;

        const rem = value % BASE91X_LEN;
        const quot = Math.floor(value / BASE91X_LEN);

        out.push(BASE91X_ALPHABET[rem]);

        if (bitCollected >= 7) {
            out.push(BASE91X_ALPHABET[quot]);
        }
    }

    return out.join("");
}


export function decode(str) {
    let collector = 0;
    let bitCollected = 0;
    let lower = -1;

    const out = [];

    for (let i = 0; i < str.length; i++) {
        const digit = BASE91X_ZYX[str.charCodeAt(i)];
        if (digit === -1) continue;

        if (lower === -1) {
            lower = digit;
            continue;
        }

        collector |= (BASE91X_LEN * digit + lower) << bitCollected;
        bitCollected += B91WORD_BIT;
        lower = -1;

        while (bitCollected >= CHAR_BIT) {
            out.push(collector & 0xFF);
            collector >>= CHAR_BIT;
            bitCollected -= CHAR_BIT;
        }
    }
    if (lower !== -1) {
        collector |= lower << bitCollected;
        bitCollected += (CHAR_BIT - 1);
    }

    if (bitCollected >= CHAR_BIT) {
        out.push(collector & 0xFF);
    }

    return Uint8Array.from(out);
}

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
package base91x;

public final class Base91x {

    private Base91x() {}

    // --- constants ---

    private static final int BASE = 91;
    private static final int CHAR_BITS = 8;
    private static final int WORD_BITS = 13;
    private static final int WORD_MASK = 0x1FFF;

    // --- alphabet ---

    private static final byte[] ALPHABET = new byte[] {
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
    };

    private static final int[] REVERSE = new int[256];

    static {
        for (int i = 0; i < REVERSE.length; i++) {
            REVERSE[i] = -1;
        }
        for (int i = 0; i < ALPHABET.length; i++) {
            REVERSE[ALPHABET[i] & 0xFF] = i;
        }
    }

    // --- size helpers ---

    public static int computeEncodedSize(int size) {
        size <<= 4;
        return (size % WORD_BITS != 0)
                ? (size / WORD_BITS + 1)
                : (size / WORD_BITS);
    }

    public static int assumeDecodedSize(int size) {
        size *= WORD_BITS;
        size >>= 4;
        return size;
    }

    // --- encode ---

    public static byte[] encode(byte[] input) {
        if (input == null) return null;

        byte[] out = new byte[computeEncodedSize(input.length)];

        int outPos = 0;
        int collector = 0;
        int bits = 0;

        for (byte b : input) {
            collector |= (b & 0xFF) << bits;
            bits += CHAR_BITS;

            while (bits >= WORD_BITS) {
                int value = collector & WORD_MASK;

                int rem = value % BASE;
                int quot = value / BASE;

                out[outPos++] = ALPHABET[rem];
                if (outPos >= out.length) break;

                out[outPos++] = ALPHABET[quot];

                collector >>>= WORD_BITS;
                bits -= WORD_BITS;
            }
        }

        if (bits > 0 && outPos < out.length) {
            int value = collector & WORD_MASK;

            int rem = value % BASE;
            int quot = value / BASE;

            out[outPos++] = ALPHABET[rem];

            if (bits >= 7 && outPos < out.length) {
                out[outPos++] = ALPHABET[quot];
            }
        }

        if (outPos == out.length) {
            return out;
        }

        // trim (Java-style)
        byte[] result = new byte[outPos];
        System.arraycopy(out, 0, result, 0, outPos);
        return result;
    }

    // --- decode ---

    public static byte[] decode(byte[] input) {
        if (input == null) return null;

        byte[] out = new byte[assumeDecodedSize(input.length)];

        int outPos = 0;
        int collector = 0;
        int bits = 0;
        int lower = -1;

        for (byte b : input) {
            int digit = REVERSE[b & 0xFF];
            if (digit == -1) continue;

            if (lower == -1) {
                lower = digit;
                continue;
            }

            collector |= (BASE * digit + lower) << bits;
            bits += WORD_BITS;
            lower = -1;

            while (bits >= CHAR_BITS && outPos < out.length) {
                out[outPos++] = (byte) (collector & 0xFF);
                collector >>>= CHAR_BITS;
                bits -= CHAR_BITS;
            }
        }

        if (lower != -1) {
            collector |= lower << bits;
            bits += (CHAR_BITS - 1);
        }

        if (bits >= CHAR_BITS && outPos < out.length) {
            out[outPos++] = (byte) (collector & 0xFF);
        }

        byte[] result = new byte[outPos];
        System.arraycopy(out, 0, result, 0, outPos);
        return result;
    }
}
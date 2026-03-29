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

    private Base91x() {
    }

    private static final int BASE = 91;
    private static final int CHAR_BITS = 8;
    private static final int WORD_BITS = 13;
    private static final int WORD_MASK = 0x1FFF;

    private static final byte[] BASE91X_ALPHABET = new byte[] {
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

    private static final byte[] BASE91X_ZYX = new byte[] {
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
    };

    public static int computeEncodedSize(int size) {
        size <<= 4;
        if (0 != size % WORD_BITS) {
            size /= WORD_BITS;
            size += 1;
        } else {
            size /= WORD_BITS;
        }
        return size;
    }

    public static int assumeDecodedSize(int size) {
        size *= WORD_BITS;
        size >>= 4;
        return size;
    }

    public static byte[] encode(byte[] input) {
        if (null == input)
            return null;

        byte[] out = new byte[computeEncodedSize(input.length)];

        int outPos = 0;
        int collector = 0;
        int bits = 0;

        for (byte b : input) {
            collector |= (b & 0xFF) << bits;
            bits += CHAR_BITS;

            while (WORD_BITS <= bits) {
                int value = collector & WORD_MASK;

                int quot = value / BASE;
                int rem = value % BASE;

                out[outPos++] = BASE91X_ALPHABET[rem];
                if (outPos >= out.length)
                    break;

                out[outPos++] = BASE91X_ALPHABET[quot];

                collector >>>= WORD_BITS;
                bits -= WORD_BITS;
            }
        }

        if (0 < bits && outPos < out.length) {
            int value = collector & WORD_MASK;

            int rem = value % BASE;
            int quot = value / BASE;

            out[outPos++] = BASE91X_ALPHABET[rem];

            if (7 <= bits && outPos < out.length) {
                out[outPos++] = BASE91X_ALPHABET[quot];
            }
        }

        if (out.length == outPos) {
            return out;
        }

        byte[] result = new byte[outPos];
        System.arraycopy(out, 0, result, 0, outPos);
        return result;
    }

    public static byte[] decode(byte[] input) {
        if (null == input)
            return null;

        byte[] out = new byte[assumeDecodedSize(input.length)];

        int outPos = 0;
        int collector = 0;
        int bits = 0;
        int lower = -1;

        for (byte b : input) {
            int digit = BASE91X_ZYX[b & 0xFF];
            if (-1 == digit)
                continue;

            if (-1 == lower) {
                lower = digit;
                continue;
            }

            collector |= (BASE * digit + lower) << bits;
            bits += WORD_BITS;
            lower = -1;

            while (CHAR_BITS <= bits && outPos < out.length) {
                out[outPos++] = (byte) (collector & 0xFF);
                collector >>>= CHAR_BITS;
                bits -= CHAR_BITS;
            }
        }

        if (-1 != lower) {
            collector |= lower << bits;
            bits += (CHAR_BITS - 1);
        }

        if (CHAR_BITS <= bits && outPos < out.length) {
            out[outPos++] = (byte) (collector & 0xFF);
        }

        byte[] result = new byte[outPos];
        System.arraycopy(out, 0, result, 0, outPos);
        return result;
    }
}

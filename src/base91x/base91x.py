"""Base91x encoder-decoder
MIT License

Copyright (c) 2022 Roman Babenko

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
"""

# BASE91X_ALPHABET in order
BASE91X_ALPHABET = "!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%"

# Base of the numeric system is 91 dec equals ASCII symbol [
BASE91X_LEN = 91

# Bits in one byte. Should be 8
CHAR_BIT = 8

# Pair of base91x symbols might code 13 bits
BASE91X_WORD_BIT = 13

# 8192 possibly values for 13 bits
BASE91X_WORD_SIZE = 0x2000

# Mask for 13 bits
BASE91X_WORD_MASK = 0x1FFF

# BASE91X reverse table for quick decoding
BASE91X_ZYX = [
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  #
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  #
    -1, 0, -1, 35, 88, 90, 89, -1, 87, 86, 85, 84, 83, 82, 81, 80,  #
    79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64,  #
    63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48,  #
    47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, -1, 34, 33, 32,  #
    31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,  #
    15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, -1]

ZYX_LEN = len(BASE91X_ZYX)

ZYX_MASK = ZYX_LEN - 1


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def encode(data: bytes) -> str:
    """Encodes bytes to base91x text

    Args:
        data: input bytes
    Return:
        string with encoded data
    """
    text = ""

    collector: int = 0
    bit_collected: int = 0
    for i in data:
        collector |= i << bit_collected
        bit_collected += CHAR_BIT
        while BASE91X_WORD_BIT <= bit_collected:
            cod = BASE91X_WORD_MASK & collector
            quotient, remainder = divmod(cod, BASE91X_LEN)
            text += BASE91X_ALPHABET[remainder]
            text += BASE91X_ALPHABET[quotient]
            collector >>= BASE91X_WORD_BIT
            bit_collected -= BASE91X_WORD_BIT

    if 0 != bit_collected:
        cod = BASE91X_WORD_MASK & collector
        quotient, remainder = divmod(cod, BASE91X_LEN)
        text += BASE91X_ALPHABET[remainder]
        if 7 <= bit_collected:
            text += BASE91X_ALPHABET[quotient]
    return text


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def decode(text: str) -> bytearray:
    """Decodes text with the base91x algorithm, skipping wrong symbols

    Args:
        text: input string with encoded data
    Return:
        decoded bytes
    """

    data = bytearray()
    collector: int = 0
    bit_collected: int = 0
    lower: int = -1
    for symbol in text:
        i = ord(symbol)
        if ZYX_MASK < i:
            continue
        digit = BASE91X_ZYX[ZYX_MASK & i]
        if -1 == digit:
            continue
        if -1 == lower:
            lower = digit
            continue

        collector |= (BASE91X_LEN * digit + lower) << bit_collected
        bit_collected += BASE91X_WORD_BIT
        lower = -1

        while CHAR_BIT <= bit_collected:
            data.append(0xFF & collector)
            collector >>= CHAR_BIT
            bit_collected -= CHAR_BIT

    if -1 != lower:
        collector |= lower << bit_collected
        bit_collected += 7  # CHAR_BIT - 1

    if CHAR_BIT <= bit_collected:
        data.append(0xFF & collector)

    return data

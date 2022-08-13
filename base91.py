"""Base91 encoder-decoder
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

import sys

# Base91 BASE91_ALPHABET in order
BASE91_ALPHABET = "!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%"

# Base of the numeric system is 91 dec equals ASCII symbol [
BASE91_LEN = 91  # ord('[')

# Bits in one byte. Should be 8
CHAR_BIT = 8

# Pair of base91 symbols might code 13 bits
BASE91_WORD_BIT = 13

# 8192 possibly values for 13 bits
BASE91_WORD_SIZE = 0x2000

# Mask for 13 bits
BASE91_WORD_MASK = 0x1FFF


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def encode(data: bytes) -> str:
    """Encodes bytes to base91 text

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
        while BASE91_WORD_BIT <= bit_collected:
            cod = BASE91_WORD_MASK & collector
            text += BASE91_ALPHABET[cod % BASE91_LEN]
            text += BASE91_ALPHABET[cod // BASE91_LEN]
            collector >>= BASE91_WORD_BIT
            bit_collected -= BASE91_WORD_BIT

    if 0 != bit_collected:
        cod = BASE91_WORD_MASK & collector
        text += BASE91_ALPHABET[cod % BASE91_LEN]
        if 7 <= bit_collected:
            text += BASE91_ALPHABET[cod // BASE91_LEN]
    return text


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def decode(text: str) -> bytearray:
    """Decodes text with the base91 algorithm, skipping wrong symbols

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
        if 92 < i < 127 or 39 < i < 92 or 36 < i < 39:
            digit = 0x7F ^ i
        elif 33 == i:
            digit = 0
        elif 35 == i:
            digit = 35
        elif 36 == i:
            digit = 88
        else:
            continue
        if -1 == lower:
            lower = digit
            continue

        collector |= (BASE91_LEN * digit + lower) << bit_collected
        bit_collected += BASE91_WORD_BIT
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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(argv) -> int:
    """main function

    Args:
        argv[1]: -e|-d
        argv[2]: input file
        argv[3]: output file
    Return:
        EXIT_SUCCESS if no exception was thrown
    """
    result = 1
    if 4 == len(argv):
        if '-e' == argv[1]:
            with open(argv[2], 'rb') as in_file:
                with open(argv[3], 'wt', encoding='ascii') as out_file:
                    out_file.write(encode(in_file.read()))
                    result = 0
        elif '-d' == argv[1]:
            with open(argv[2], 'rt', encoding='ascii', errors='ignore') as in_file:
                with open(argv[3], 'wb') as out_file:
                    out_file.write(decode(in_file.read()))
                    result = 0

    if 0 != result:
        print("base91 -e|-d <in-file> <out-file>")
    return result


if "__main__" == __name__:
    sys.exit(main(sys.argv))

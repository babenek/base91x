"""
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

# Base91 alphabet in order
alphabet = "!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%"

# Base of the numeric system is 91 dec equals ASCII symbol [
base = ord('[')

# Bits in one byte. Should be 8
char_bit = 8

# Pair of base91 symbols might code 13 bits
b91word_bit = 13

# 8192 possibly values for 13 bits
b91word_size = 0x2000

# Mask for 13 bits
b91word_mask = 0x1FFF


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
    for n in data:
        collector |= n << bit_collected
        bit_collected += char_bit
        while b91word_bit <= bit_collected:
            cod = b91word_mask & collector
            text += alphabet[cod % base]
            text += alphabet[cod // base]
            collector >>= b91word_bit
            bit_collected -= b91word_bit

    if 0 != bit_collected:
        cod = b91word_mask & collector
        text += alphabet[cod % base]
        if 7 <= bit_collected:
            text += alphabet[cod // base]
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
        x = ord(symbol)
        if 92 < x < 127 or 39 < x < 92 or 36 < x < 39:
            digit = 0x7F ^ x
        elif 33 == x:
            digit = 0
        elif 35 == x:
            digit = 35
        elif 36 == x:
            digit = 88
        else:
            continue
        if -1 == lower:
            lower = digit
            continue

        collector |= (base * digit + lower) << bit_collected
        bit_collected += b91word_bit
        lower = -1

        while char_bit <= bit_collected:
            data.append(0xFF & collector)
            collector >>= char_bit
            bit_collected -= char_bit

    if -1 != lower:
        collector |= lower << bit_collected
        bit_collected += 7  # char_bit - 1

    if char_bit <= bit_collected:
        data.append(0xFF & collector)

    return data


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(argv) -> int:
    """main function
    argv[1]: -e|-d
    argv[2]: input file
    argv[3]: output file
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

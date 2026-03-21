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

#include <limits.h>
#include <stdlib.h>

#if CHAR_BIT != 8
#error DESIGNED ONLY FOR 8 BIT BYTE (CHAR)
#endif

_Static_assert(24 > sizeof(unsigned), "unsigned must be 24 bits or more");

#include "base91x.h"

/** Base of the numeric system is 91dec equals ASCII symbol [ */
#define BASE91X_LEN 91

/** Bits in one byte. Should be 8 */
static const unsigned char_bit = CHAR_BIT;

/** Each pair of base91x symbols encodes 13 bits */
static const unsigned b91word_bit = 13;

/** Mask for 13 bits */
static const unsigned b91word_mask = 0x1FFF;

/** base91x JSON OPTIMIZED ALPHABET: */
// clang-format off
static const unsigned char BASE91X_ALPHABET[BASE91X_LEN] = {'!', '~', '}', '|', '{', 'z', 'y', 'x', 'w', 'v',
                                                            'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l',
                                                            'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b',
                                                            'a', '`', '_', '^', ']', '#', '[', 'Z', 'Y', 'X',
                                                            'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N',
                                                            'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D',
                                                            'C', 'B', 'A', '@', '?', '>', '=', '<', ';', ':',
                                                            '9', '8', '7', '6', '5', '4', '3', '2', '1', '0',
                                                            '/', '.', '-', ',', '+', '*', ')', '(', '$', '&',
                                                            '%'};
// clang-format on

/** base91x reverse table for quick decoding from an 8-bit unsigned index */
// clang-format off
static const char BASE91X_ZYX[0x100] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        -1, 0,  -1, 35, 88, 90, 89, -1, 87, 86, 85, 84, 83, 82, 81, 80,
                                        79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64,
                                        63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48,
                                        47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, -1, 34, 33, 32,
                                        31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
                                        15, 14, 13, 12, 11, 10, 9,  8,  7,  6,  5,  4,  3,  2,  1,  -1,
                                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                        };
// clang-format on

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

size_t compute_encoded_size(size_t size)
{
    size <<= 4;
    if (0 != size % b91word_bit)
    {
        size /= b91word_bit;
        size += 1;
    }
    else
    {
        size /= b91word_bit;
    }
    return size;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

size_t assume_decoded_size(size_t size)
{
    size *= b91word_bit;
    size >>= 4;
    return size;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

int base91x_encode(
    const unsigned char *in_ptr,
    const size_t in_size,
    unsigned char *out_ptr,
    const size_t out_size)
{
    const unsigned char *const in_ptr_end = in_ptr + in_size;
    const unsigned char *const out_ptr_end = out_ptr + out_size;

    unsigned collector = 0;
    unsigned bit_collected = 0;

    while (in_ptr < in_ptr_end && out_ptr < out_ptr_end)
    {
        collector |= (*in_ptr) << bit_collected;
        ++in_ptr;
        bit_collected += char_bit;
        while (b91word_bit <= bit_collected)
        {
            div_t d = div(b91word_mask & collector, BASE91X_LEN);
            *out_ptr = BASE91X_ALPHABET[d.rem];
            if (++out_ptr == out_ptr_end)
                return 2;
            *out_ptr = BASE91X_ALPHABET[d.quot];
            ++out_ptr;
            collector >>= b91word_bit;
            bit_collected -= b91word_bit;
        }
    }

    if (0 != bit_collected)
    {
        if (out_ptr_end <= out_ptr)
            return 4;
        const div_t d = div(b91word_mask & collector, BASE91X_LEN);
        *out_ptr = BASE91X_ALPHABET[d.rem];
        if (7 <= bit_collected)
        {
            if (++out_ptr == out_ptr_end)
                return 6;
            *out_ptr = BASE91X_ALPHABET[d.quot];
        }
    }
    if (in_ptr == in_ptr_end && out_ptr <= out_ptr_end)
        return 0;
    return 1;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

int base91x_decode(
    const unsigned char *in_ptr,
    const size_t in_size,
    unsigned char *out_ptr,
    size_t *out_size)
{
    const unsigned char *const in_ptr_end = in_ptr + in_size;
    const unsigned char *const out_ptr_end = out_ptr + *out_size;
    unsigned char *out_ptr_start = out_ptr;

    unsigned collector = 0;
    unsigned bit_collected = 0;
    char lower = -1;

    while (in_ptr < in_ptr_end && out_ptr < out_ptr_end)
    {
        const char digit = BASE91X_ZYX[*in_ptr];
        ++in_ptr;
        if (-1 == digit)
            continue;
        if (-1 == lower)
        {
            lower = digit;
            continue;
        }

        collector |= (BASE91X_LEN * digit + lower) << bit_collected;
        bit_collected += b91word_bit;
        lower = -1;

        while (char_bit <= bit_collected && out_ptr < out_ptr_end)
        {
            *out_ptr = 0xFF & collector;
            ++out_ptr;
            collector >>= char_bit;
            bit_collected -= char_bit;
        }
    }

    if (-1 != lower)
    {
        collector |= lower << bit_collected;
        bit_collected += (char_bit - 1);
    }

    if (char_bit <= bit_collected && out_ptr < out_ptr_end)
    {
        *out_ptr = 0xFF & collector;
        ++out_ptr;
    }

    if (in_ptr_end == in_ptr && out_ptr <= out_ptr_end)
    {
        *out_size = (out_ptr - out_ptr_start);
        return 0;
    }
    return 1;
}

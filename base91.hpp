/*
MIT License

Copyright (c) 2017 Roman Babenko

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

#pragma once

#include <vector>
#include <string>
//#include <cstdlib>

#if __CHAR_BIT__ != 8
#error DESIGNED ONLY FOR 8 BIT BYTE (CHAR)
#endif

//------------------------------------------------------------------------------
/**
 * Class base91 provides encoding and decoding statics methods
 * using numeric system of base 91 with specific alphabet that does not require
 * escaping any symbols in C, C++ string.
 * The alphabet contains printable characters of ASCII except:
 * " Quotation mark
 * ' Apostrophe
 * \ Backslash
 * An encoded string might be used for JSON string if JSON does not require
 * to escate / Slash.
 * Encoded string size ~ 1.231 * original size.
 * There is possibility to extend the algorithm to use 89 codes during decode.
 */

class base91
{
public:
    /** Base of the numeric system is 91dec equals ASCII symbol [ */
    static const char BASE91_LEN = 91;

    /** Bits in one byte. Should be 8 */
    static const unsigned char_bit = __CHAR_BIT__;

    /** Pair of base91 symbols might code 13 bits */
    static const unsigned b91word_bit = 13;

    /** 8192 possibly values for 13 bits */
    static const unsigned b91word_size = 0x2000;

    /** Mask for 13 bits */
    static const unsigned b91word_mask = 0x1FFF;

    /** BASE91 JSON OPTIMIZED ALPHABET: */
    static constexpr unsigned char BASE91_ALPHABET[BASE91_LEN] = {'!', '~', '}', '|', '{', 'z', 'y', 'x', 'w', 'v',
        'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', '`',
        '_', '^', ']', '#', '[', 'Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J',
        'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A', '@', '?', '>', '=', '<', ';', ':', '9', '8', '7', '6', '5', '4',
        '3', '2', '1', '0', '/', '.', '-', ',', '+', '*', ')', '(', '$', '&', '%'};

    /** BASE91 reverse table for quick decoding */
    static constexpr char BASE91_ZYX[0x80] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 35, 88, 90, 89, -1, 87, 86, 85, 84, 83,
        82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56,
        55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, -1, 34, 33, 32, 31, 30, 29,
        28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, -1};

    /**
     * Calculate exactly size required for encoded data
     * @param size - size of data to encoding
     * @return size of encoded data
     */
    static inline size_t compute_encoded_size(size_t size)
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

    /**
     * Assume maximal size for decoded data
     * Final size may be less due some of symbols are skipped
     * @param size - size of data to decoding
     * @return maximal size of decoded data
     */
    static inline size_t assume_decoded_size(size_t size)
    {
        size *= b91word_bit;
        size >>= 4;
        return size;
    }

    /**
     * Encode 8bit based container(vector) to string
     * @param data[IN] - 8bit based std::vector
     * @param text[OUT] - std::string
     * @param dummy - do not use
     */
    template <typename Container>
    static void encode(const Container &data, std::string &text,
        typename std::enable_if<sizeof(typename Container::value_type) == sizeof(char)>::type *dummy = nullptr)
    {
        text.clear();
        text.reserve(compute_encoded_size(data.size()));

        unsigned collector = 0;
        unsigned bit_collected = 0;

        for (auto &i : data)
        {
            collector |= static_cast<unsigned char>(i) << bit_collected;
            bit_collected += char_bit;
            while (b91word_bit <= bit_collected)
            {
                div_t d = std::div(b91word_mask & collector, BASE91_LEN);
                text.push_back(BASE91_ALPHABET[d.rem]);
                text.push_back(BASE91_ALPHABET[d.quot]);
                collector >>= b91word_bit;
                bit_collected -= b91word_bit;
            }
        }

        if (0 != bit_collected)
        {
            const div_t d = std::div(b91word_mask & collector, BASE91_LEN);
            text.push_back(BASE91_ALPHABET[d.rem]);
            if (7 <= bit_collected)
                text.push_back(BASE91_ALPHABET[d.quot]);
        }
    }

    /**
     * Decode string to binary std::vector
     * @param text[IN] - std::string
     * @param data[OUT] - std::vector of 8bit elements
     * @param dummy - do not use
     */
    template <typename Container>
    static void decode(const std::string &text, Container &data,
        typename std::enable_if<sizeof(typename Container::value_type) == sizeof(char)>::type *dummy = nullptr)
    {
        data.clear();
        data.reserve(assume_decoded_size(text.size()));

        unsigned collector = 0;
        unsigned bit_collected = 0;
        char lower = -1;

        for (auto &i : text)
        {
            const char digit = BASE91_ZYX[0x7F & i];
            if (-1 == digit)
            {
                continue;
            }
            if (-1 == lower)
            {
                lower = digit;
                continue;
            }

            collector |= (BASE91_LEN * digit + lower) << bit_collected;
            bit_collected += b91word_bit;
            lower = -1;

            while (char_bit <= bit_collected)
            {
                data.push_back(static_cast<unsigned char>(0xFF & collector));
                collector >>= char_bit;
                bit_collected -= char_bit;
            }
        }

        if (-1 != lower)
        {
            collector |= lower << bit_collected;
            bit_collected += (char_bit - 1);
        }

        if (char_bit <= bit_collected)
            data.push_back(static_cast<unsigned char>(0xFF & collector));
    }
};

//------------------------------------------------------------------------------

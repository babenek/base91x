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
private:
    /** BASE91 JSON OPTIMIZED ALPHABET: */
    static constexpr unsigned char BASE91_ALPHABET[]
        = "!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%";

    /** Base of the numeric system is 91dec equals ASCII symbol [ */
    static const char BASE91_LEN = 91; // '['

    /** Bits in one byte. Should be 8 */
    static const unsigned char_bit = __CHAR_BIT__;

    /** Pair of base91 symbols might code 13 bits */
    static const unsigned b91word_bit = 13;

    /** 8192 possibly values for 13 bits */
    static const unsigned b91word_size = 0x2000;

    /** Mask for 13 bits */
    static const unsigned b91word_mask = 0x1FFF;

public:
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
        size *= 13;
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
        text.reserve(compute_encoded_size(data.size()));

        unsigned collector = 0;
        unsigned bit_collected = 0;

        for (auto &n : data)
        {
            collector |= static_cast<unsigned char>(n) << bit_collected;
            bit_collected += char_bit;
            while (b91word_bit <= bit_collected)
            {
                const unsigned cod = b91word_mask & collector;
                text.push_back(BASE91_ALPHABET[cod % BASE91_LEN]);
                text.push_back(BASE91_ALPHABET[cod / BASE91_LEN]);
                collector >>= b91word_bit;
                bit_collected -= b91word_bit;
            }
        }

        if (0 != bit_collected)
        {
            const unsigned cod = b91word_mask & collector;
            text.push_back(BASE91_ALPHABET[cod % BASE91_LEN]);
            if (7 <= bit_collected)
                text.push_back(BASE91_ALPHABET[cod / BASE91_LEN]);
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
        data.reserve(assume_decoded_size(text.size()));

        unsigned collector = 0;
        unsigned bit_collected = 0;
        char lower = -1;

        for (auto &i : text)
        {
            char digit = -1;
            if ((92 < i and i < 127) or (39 < i and  i< 92) or (36 < i and i< 39))
                digit = 0x7F ^ i;
            else if (33 == i)
                digit = 0;
            else if (35 == i)
                digit = 35;
            else if (36 == i)
                digit = 88;
            else
                continue;
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

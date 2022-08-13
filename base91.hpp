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
    /*
    BASE91 JSON OPTIMIZED ALPHABET:
!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-+*)($&%
    */
    /** Base of the numeric system is 91dec equals ASCII symbol [ */
    static const char base = '[';

    /** Bits in one byte. Should be 8 */
    static const unsigned char_bit = __CHAR_BIT__;

    /** Pair of base91 symbols might code 13 bits */
    static const unsigned b91word_bit = 13;

    /** 8192 possibly values for 13 bits */
    static const unsigned b91word_size = 0x2000;

    /** Mask for 13 bits */
    static const unsigned b91word_mask = 0x1FFF;

protected:
    /**
     * Convert number 0 - 90 to symbol
     * @param a[in] - number 0 - 90
     * @return symbol from alphabet or -1 if input is out of alphabet
     */
    static inline char encodeSymbol(const char a)
    {
        switch (a)
        {
            case '\0':
                return '!';
                break;
            case '#':
                return '#';
                break;
            case 'X':
                return '$';
                break;
            default:
                if ('\0' <= a and base > a)
                {
                    return 0x7F ^ a;
                }
                break;
        }
        return -1;
    }

    /**
     * Convert base91 symbol to decimal values
     * @param a[in] - any symbol
     * @return 0-90 if symbol is in alphabet -1 - in other case
     */
    static inline char decodeSymbol(const char a)
    {
        switch (a)
        {
            case '!': {
                return '\0';
            }
            break;
            case '#': {
                return '#';
            }
            break;
            case '$': {
                return 'X';
            }
            break;
            default: {

                if ('!' <= a and '~' >= a and '\'' != a and '\"' != a and '\\' != a)
                {
                    return 0x7F ^ a;
                }
            }
            break;
        }
        return -1;
    }

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
     * @param in - 8bit based std::vector
     * @param out - std::string
     * @param dummy - do not use
     */
    template <typename Container>
    static void encode(const Container &in, std::string &out,
        typename std::enable_if<sizeof(typename Container::value_type) == sizeof(char)>::type *dummy = nullptr)
    {
        out.reserve(compute_encoded_size(in.size()));

        auto HI = new char[b91word_size];
        auto LO = new char[b91word_size];
        {
            // initialize encoder
            char hi = 0;
            char lo = 0;
            unsigned n = 0;
            while (n < b91word_size)
            {
                LO[n] = encodeSymbol(lo);
                HI[n] = encodeSymbol(hi);
                if (base == (++lo))
                {
                    lo = 0;
                    hi++;
                }
                n++;
            }
        }

        unsigned collector = 0;
        unsigned bit_collected = 0;

        for (auto &n : in)
        {
            collector |= static_cast<unsigned char>(n) << bit_collected;
            bit_collected += char_bit;
            while (b91word_bit <= bit_collected)
            {
                const unsigned cod = b91word_mask & collector;
                out.push_back(LO[cod]);
                out.push_back(HI[cod]);
                collector >>= b91word_bit;
                bit_collected -= b91word_bit;
            }
        }

        if (0 != bit_collected)
        {
            const unsigned cod = b91word_mask & collector;
            out.push_back(LO[cod]);
            if (7 <= bit_collected)
            {
                out.push_back(HI[cod]);
            }
        }

        delete[] LO;
        delete[] HI;

        return;
    }

    /**
     * Decode string to binary std::vector
     * @param in - std::string
     * @param out - std::vector of 8bit elements
     * @param dummy - do not use
     */
    template <typename Container>
    static void decode(const std::string &in, Container &out,
        typename std::enable_if<sizeof(typename Container::value_type) == sizeof(char)>::type *dummy = nullptr)
    {
        out.reserve(assume_decoded_size(in.size()));

        auto ZYX = new char[1 << char_bit];
        for (unsigned n = 0; n < (1 << char_bit); ++n)
        {
            // fill reverse alphabet
            ZYX[n] = decodeSymbol(n);
        }
        auto HILO = new short[base][base];
        {
            // fill reverse codes
            unsigned hi = 0;
            unsigned lo = 0;
            //            std::cerr << "[[";
            for (unsigned n = 0; n < b91word_size; ++n)
            {
                //                std::cerr << n << ",";
                HILO[hi][lo] = n;
                if (base == (++lo))
                {
                    lo = 0;
                    hi++;
                    //                    std::cerr << "]," << std::endl << "[";
                }
            }
            // subzero values to optional purpose
            for (int n = 2; n < static_cast<int>(base); ++n)
            {
                HILO[base - 1][n] = 0 - n;
                //                std::cerr << 0 - n << ",";
            }
            //            std::cerr << "]]" << std::endl;
        }

        unsigned collector = 0;
        int bit_collected = 0;
        char lower = -1;

        for (auto &n : in)
        {
            const char digit = ZYX[n];
            if (-1 == digit)
            {
                continue;
            }
            if (-1 == lower)
            {
                lower = digit;
                continue;
            }
            const short cod = HILO[digit][lower];
            if ((b91word_mask & cod) != cod)
            {
                lower = -1;
                continue;
                // there is possibility to use 89 subzero values as codes
            }
            collector |= cod << bit_collected;
            bit_collected += b91word_bit;
            lower = -1;

            while (char_bit <= bit_collected)
            {
                out.push_back(static_cast<char>(0xFF & collector));
                collector >>= char_bit;
                bit_collected -= char_bit;
            }
        }

        if (-1 != lower)
        {
            collector |= HILO[0][lower] << bit_collected;
            bit_collected += (char_bit - 1);
        }

        if (char_bit <= bit_collected)
        {
            out.push_back(static_cast<char>(0xFF & collector));
        }

        delete[] HILO;
        delete[] ZYX;
    }
};

//------------------------------------------------------------------------------

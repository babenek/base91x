/*
MIT License

Copyright (c) 2023 Roman Babenko

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
#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <cmath>

#include "base91x.hpp"

#define LOG std::cerr << "L_" << __LINE__ << ": "

//------------------------------------------------------------------------------

bool in_abc(char i)
{
    return ((92 < i and i < 127) or (39 < i and i < 92) or (36 < i and i < 39) or 33 == i or 35 == i or 36 == i);
}

//------------------------------------------------------------------------------

bool test_alphabets()
{
    if (91 != sizeof(base91x::BASE91X_ALPHABET))
    {
        LOG << "Wrong size of direct alphabet "<<  sizeof(base91x::BASE91X_ALPHABET) << std::endl;
        return false;
    }

    if (0x80 != sizeof(base91x::BASE91X_ZYX))
    {
        LOG << "Wrong size of reverse alphabet" << std::endl;
        return false;
    }

    for (unsigned n = 0; n < sizeof(base91x::BASE91X_ZYX); ++n)
    {
        char digit = -2;
        if ((92 < n and n < 127) or (39 < n and n < 92) or (36 < n and n < 39))
            digit = 0x7F ^ n;
        else if (33 == n)
            digit = 0;
        else if (35 == n)
            digit = 35;
        else if (36 == n)
            digit = 88;
        else
            digit = -1;

        if (digit != base91x::BASE91X_ZYX[n])
        {
            LOG << "error on " << n << " element" << std::endl;
            return false;
        }
    }
    for (auto &i : base91x::BASE91X_ALPHABET)
    {
        if (sizeof(base91x::BASE91X_ZYX) <= i)
        {
            LOG << "out of size " << (i) << " element" << std::endl;
            return false;
        }
        if (0 > base91x::BASE91X_ZYX[i])
        {
            LOG << "error on " << i << " element" << std::endl;
            return false;
        }
        if (not in_abc(i))
        {
            LOG << "wrong " << i << " element" << std::endl;
            return false;
        }
    }

    //        const char digit = BASE91X_ZYX[0x7F & i];

    LOG << "Alphabets tests passed" << std::endl;
    return true;
}

//------------------------------------------------------------------------------

template <typename T>
bool test_refurbish(const size_t size)
{
    T data_original(size);
    std::generate(data_original.begin(), data_original.end(), std::rand);

    std::string text;
    base91x::encode(data_original, text);

    size_t n = 0;
    // verify whether encoded text contains symbols from base91x alphabet only
    for (auto it_text : text)
    {
        if (not in_abc(it_text))
        {
            LOG << "error on " << n << " element '" << it_text << "' not in base91x::BASE91X_ALPHABET" << std::endl;
            return false;
        }
        ++n;
    }

    LOG << "Test with data [" << data_original.size() << "] -> encoded text [" << text.size() << "]" << std::endl;
    if (80 < text.size())
    {
        LOG << "Limit to first 80 symbols:" << std::endl << text.substr(1, 79) << std::endl;
    }
    else
    {
        LOG << text << std::endl;
    }

    T data_refurbed;
    base91x::decode(text, data_refurbed);

    if (data_original.size() != data_refurbed.size())
    {
        LOG << "data_original size (" << data_original.size() << ") does not equal data_refurbed size ("
            << data_refurbed.size() << ")" << std::endl;
        return false;
    }

    n = 0;
    auto it_original = data_original.begin();
    auto it_refurbed = data_refurbed.begin();
    while (it_original != data_original.end() and it_refurbed != data_refurbed.end())
    {
        if (*it_original != *it_refurbed)
        {
            LOG << "error on " << n << " element" << std::endl;
            return false;
        }
        ++n;
        ++it_original;
        ++it_refurbed;
    }
    LOG << "Test passed with size = " << data_original.size() << std::endl;

    if (base91x::compute_encoded_size(size) != text.size())
    {
        LOG << "computed " << base91x::compute_encoded_size(size) << " != " << text.size() << std::endl;
        return false;
    }

    if (base91x::assume_decoded_size(text.size()) != size)
    {
        LOG << "assumed " << base91x::assume_decoded_size(size) << " != " << text.size() << std::endl;
        return false;
    }

    return true;
}

//------------------------------------------------------------------------------

bool test_static_with_space()
{
    const std::string_view pangram_test = "* / * / *The quick brown fox\tjumps\nover\rthe lazy dog { < # > }";
    const std::string pangram_expected = "*/*/*Thequickbrownfoxjumpsoverthelazydog{<#>}";
    std::vector<unsigned char> data;
    base91x::decode(pangram_test, data);

    const std::vector<unsigned char> data_expected = {197, 188, 152, 123, 190, 170, 196, 57, 20, 212, 152, 234, 45,
        19, 38, 185, 248, 29, 56, 51, 69, 134, 70, 46, 193, 65, 219, 166, 60, 124, 38, 76, 84, 125, 125, 174};

    if (data_expected.size() != data.size())
    {
        LOG << "data size = " << data.size() << ": expected size = " << data_expected.size() << std::endl;
        return false;
    }

    size_t n = 0;
    auto it = data.begin();
    auto it_ = data_expected.begin();
    while (it != data.end() and it_ != data_expected.end())
    {
        if (*it != *it_)
        {
            LOG << "Error on " << n << " element. got " << int(*it_) << " expected " << int(*it) << std::endl;
            return false;
        }
        ++n;
        ++it;
        ++it_;
    }

    if (data.size() != n)
    {
        LOG << "Pass only " << n << "bytes. Expected " << data.size() << std::endl;
        return false;
    }

    std::string pangram_refurb;
    base91x::encode(data, pangram_refurb);

    if (pangram_expected != pangram_refurb)
    {
        LOG << "Not matched" << std::endl << pangram_expected << std::endl << pangram_refurb << std::endl;
        return false;
    }
    LOG << "Static test passed" << std::endl;
    return true;
}

//------------------------------------------------------------------------------

bool test_stress(const size_t size)
{
    std::string text;
    text.resize(size);
    std::generate(text.begin(), text.end(), std::rand);
    std::vector<unsigned char> data;
    base91x::decode(text, data);
    LOG << "Stress test: from " << size << " symbols were decoded " << data.size() << " bytes" << std::endl;
    LOG << "Stress test passed" << std::endl;
    return true;
}

//------------------------------------------------------------------------------

int main(const int argc, const char *argv[])
{
    std::srand(std::time(nullptr));
    // various size of random data to cover all possibly calculated size
    for (int n = 0; n < 33; ++n)
    {
        if (not( //
                test_refurbish<std::vector<char>>(n) //
                && //
                test_refurbish<std::vector<unsigned char>>(n) //
                ))
            return 1;
    }
    // 1Mb of random data
    if ( //
        test_refurbish<std::vector<char>>(std::rand() % (1 << 20)) //
        && //
        test_refurbish<std::vector<unsigned char>>(std::rand() % (1 << 20)) //
        && //
        test_static_with_space() //
        && //
        test_alphabets() //
        && //
        test_stress(1 << 20) //
    )
    {
        return 0;
    }
    return 1;
}

//------------------------------------------------------------------------------

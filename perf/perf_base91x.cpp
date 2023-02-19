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

static const size_t LEN = 100;

//------------------------------------------------------------------------------

void time_stat_encode(const size_t size)
{
    std::vector<char> data;
    data.resize(size);
    std::generate(data.begin(), data.end(), std::rand);
    std::string text;

    long double stat[LEN] = {0};
    long double avg = 0;
    long double sum = 0;
    long double sgm = 0;

    std::cout << "encoding with " << size << " bytes " << std::endl;
    for (unsigned n = 0; n < LEN; ++n)
    {
        const std::chrono::system_clock::time_point startTime = std::chrono::system_clock::now();
        base91x::encode(data, text);
        stat[n] = 0.000000001
            * static_cast<double>(std::chrono::nanoseconds(std::chrono::system_clock::now() - startTime).count());
        sum += stat[n];
        std::cout << n << " " << std::flush;
    }

    avg = sum / LEN;

    for (unsigned n = 0; n < LEN; ++n)
        sgm += pow(avg - stat[n], 2);
    sgm /= LEN;
    sgm = sqrt(sgm);

    std::cout << "\nAverage = " << avg << " Deviation = " << sgm << std::endl;
}

//------------------------------------------------------------------------------

void time_stat_decode(const size_t size)
{
    std::vector<char> data;
    data.resize(size);
    std::generate(data.begin(), data.end(), std::rand);
    std::string text;
    base91x::encode(data, text);

    long double stat[LEN] = {0};
    long double avg = 0;
    long double sum = 0;
    long double sgm = 0;

    std::cout << "decoding with " << size << " bytes " << std::endl;
    for (unsigned n = 0; n < LEN; ++n)
    {
        const std::chrono::system_clock::time_point startTime = std::chrono::system_clock::now();
        base91x::decode(text, data);
        stat[n] = 0.000000001
            * static_cast<double>(std::chrono::nanoseconds(std::chrono::system_clock::now() - startTime).count());
        sum += stat[n];
        std::cout << n << " " << std::flush;
    }

    avg = sum / LEN;

    for (unsigned n = 0; n < LEN; ++n)
        sgm += pow(avg - stat[n], 2);
    sgm /= LEN;
    sgm = sqrt(sgm);

    std::cout << "\nAverage = " << avg << " Deviation = " << sgm << std::endl;
}

//------------------------------------------------------------------------------
int main(const int argc, const char *argv[])
{
    time_stat_encode(1 << 23);
    time_stat_decode(1 << 23);
    return 0;
}

//------------------------------------------------------------------------------

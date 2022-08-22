#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <cmath>

#include "base91.hpp"

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
        base91::encode(data, text);
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
    base91::encode(data, text);

    long double stat[LEN] = {0};
    long double avg = 0;
    long double sum = 0;
    long double sgm = 0;

    std::cout << "decoding with " << size << " bytes " << std::endl;
    for (unsigned n = 0; n < LEN; ++n)
    {
        const std::chrono::system_clock::time_point startTime = std::chrono::system_clock::now();
        base91::decode(text, data);
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

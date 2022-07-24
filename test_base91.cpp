#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <ctime>

#include "base91.h"

//------------------------------------------------------------------------------

template <typename T>
bool test_refurbish(const size_t size)
{
    T data_original(size);
    std::generate(data_original.begin(), data_original.end(), std::rand);
    std::cerr << __LINE__ << ": Run test with size = " << data_original.size() << std::endl;

    std::string text;
    base91::encode(data_original, text);
    std::cerr << __LINE__ << ": Encoded data size = " << text.size() << std::endl;

    size_t n = 80 < text.size() ? 80 : text.size();
    std::cerr << __LINE__ << ": First " << n << " symbols are:" << std::endl;

    auto lim_text = text;
    lim_text.resize(n);
    std::cerr << lim_text << std::endl;

    T data_refurbed;
    base91::decode(text, data_refurbed);

    if (data_original.size() != data_refurbed.size())
    {
        std::cerr << __LINE__ << ": data_original size (" << data_original.size()
                  << ") does not equal data_refurbed size (" << data_refurbed.size() << ")" << std::endl;
        return false;
    }

    n = 0;
    auto it_original = data_original.begin();
    auto it_refurbed = data_refurbed.begin();
    while (it_original != data_original.end() and it_refurbed != data_refurbed.end())
    {
        if (*it_original != *it_refurbed)
        {
            std::cerr << __LINE__ << ": error on " << n << " element" << std::endl;
            return false;
        }
        ++n;
        ++it_original;
        ++it_refurbed;
    }
    std::cerr << __LINE__ << ": Test passed with size = " << data_original.size() << std::endl;
    return true;
}

//------------------------------------------------------------------------------

bool test_static_with_space()
{
    std::string pangram = "The quick brown fox\tjumps\nover\rthe lazy dog";
    std::vector<unsigned char> data;
    base91::decode(pangram, data);

    if (26 != data.size())
    {
        std::cerr << __LINE__ << ": data size = " << data.size() << std::endl;
        return false;
    }

    std::vector<unsigned char> data_=//
        {0xbc,0x43,0x41,0x8d,0xa9,0xde,0x32,0x61,0x92,0x8b,0xdf,0x81,0x33
        ,0x53,0x64,0x68,0xe4,0x12,0x1c,0xb4,0x6d,0xca,0xc3,0x67,0xc2,0x44};

    size_t n = 0;
    auto it = data.begin();
    auto it_ = data_.begin();
    while (it != data.end() and it_ != data_.end())
    {
        if (*it != *it_)
        {
            std::cerr << __LINE__ << ": error on " << n << " element" << std::endl;
            return false;
        }
        ++n;
        ++it;
        ++it_;
    }

    if (data.size() != n)
    {
        std::cerr << __LINE__ << ": Pass only " << n << "bytes. Expected " << data.size() << std::endl;
        return false;
    }

    std::string pangram_;
    base91::encode(data, pangram_);

    if ("Thequickbrownfoxjumpsoverthelazydog" != pangram_)
    {
        std::cerr << __LINE__ << ":" << std::endl << pangram << std::endl << pangram_ << std::endl;
        return false;
    }
    std::cerr << __LINE__ << ": Static test passed" << std::endl;
    return true;
}

//------------------------------------------------------------------------------

int main(const int argc, const char *argv[])
{
    std::srand(std::time(nullptr));
    if ( //
        test_refurbish<std::vector<char>>(std::rand() % (1 << 20)) //
        && //
        test_refurbish<std::vector<unsigned char>>(std::rand() % (1 << 20)) //
        && //
        test_static_with_space() //
    )
        return 0;
    return 1;
}

//------------------------------------------------------------------------------

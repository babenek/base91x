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
#include <cstring>
#include <iostream>
#include <fstream>

#include "base91x.hpp"

//------------------------------------------------------------------------------

template <typename Container>
void readFile(const std::string &fileName, Container &container)
{
    std::fstream fs(fileName, std::ios::in | std::ios::binary);
    if (fs.is_open() and fs.good())
    {
        fs.seekg(0, std::ios::end);
        auto newSize = fs.tellp();
        fs.seekg(0, std::ios::beg);
        container.clear();
        container.resize(newSize);
        fs.read(&container[0], newSize);
        fs.close();
    }
    return;
}

//------------------------------------------------------------------------------

template <typename Container>
void writeFile(const std::string &fileName, const Container &container)
{
    std::fstream fs(fileName, std::ios::trunc | std::ios::out | std::ios::binary);

    if (fs.good())
    {
        fs.write(container.data(), container.size());
        fs.close();
    }
    return;
}

//------------------------------------------------------------------------------

int main(const int argc, const char *argv[])
{
    if (argc != 4 or not(0 == strncmp("-e", argv[1], 3) or 0 == strncmp("-d", argv[1], 3)))
    {
        std::cerr << "base91x -e|-d <in-file> <out-file>";
        return -1;
    }

    if (0 == strncmp("-e", argv[1], 3))
    {
        std::vector<char> in;
        std::string out;

        readFile(argv[2], in);
        base91x::encode(in, out);
        writeFile(argv[3], out);
    }
    else
    {
        std::string in;
        std::vector<char> out;

        readFile(argv[2], in);
        base91x::decode(in, out);
        writeFile(argv[3], out);
    }

    return 0;
}

//------------------------------------------------------------------------------

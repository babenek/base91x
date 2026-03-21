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
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "base91x.h"

int main()
{
    unsigned char buf[4096];
    size_t t = sizeof(buf);
    if (base91x_encode("", 0, buf, 0))
        return __LINE__;
    if (!base91x_encode("AAAA", 4, buf, 0))
        return __LINE__;
    if (base91x_encode("AAAA", 4, buf, 5))
        return __LINE__;
    if (memcmp("O|ico", buf, 5))
        return __LINE__;
    if (base91x_encode("AAAAAAAAAAAAA", 13, buf, t))
        return __LINE__;
    if (memcmp("O|ic.RzxSG:~tq)i", buf, 16))
        return __LINE__;
    if (base91x_decode("\t O | i c. R z x S G : ~t q ) \0\n i            ", 42, buf, &t))
        return __LINE__;
    if (13 != t)
        return __LINE__;
    if (memcmp("AAAAAAAAAAAAA", buf, 13))
        return __LINE__;
    printf("\nPASS\n");
    return 0;
}

// clang -O2 -Wall tests/test_base91x.c src/base91x.c -I include -o test_base91x_c && ./test_base91x_c && echo PASS

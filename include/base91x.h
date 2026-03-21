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

#ifndef BASE91X_H
#define BASE91X_H

#include <stddef.h>

#ifdef __cplusplus
extern "C"
{
#endif

    /**
     * Calculate exactly size required for encoded data
     * @param size - size of data to encoding
     * @return size of encoded data
     */
    size_t compute_encoded_size(size_t size);

    /**
     * Assume maximal size for decoded data
     * Final size may be less due some of symbols are skipped
     * @param size - size of data to decoding
     * @return maximal size of decoded data
     */
    size_t assume_decoded_size(size_t size);

    /**
     * Encode byte data to base91x
     * @param in_ptr[IN] - input data pointer
     * @param in_size[IN] - size of input buffer
     * @param out_ptr[OUT] - pointer to output buffer
     * @param out_size[OUT] - size of output buffer (must be exactly known with compute_encoded_size)
     */
    int base91x_encode(
        const unsigned char *in_ptr,
        const size_t in_size,
        unsigned char *out_ptr,
        const size_t out_size);

    /**
     * Decode input buffer from base91x encoding to bytes with skip not suitable symbols
     * @param in_ptr[IN] - input data pointer
     * @param in_size[IN] - size of input buffer
     * @param out_ptr[OUT] - pointer to output buffer
     * @param out_size[OUT] - maximal size of output buffer (should be assumed for maximal size with assume_decoded_size)
     */
    int base91x_decode(
        const unsigned char *in_ptr,
        const size_t in_size,
        unsigned char *out_ptr,
        size_t *out_size);

#ifdef __cplusplus
}
#endif

#endif /* BASE91X_H */
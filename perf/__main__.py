"""
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
"""
import math
import random
import sys
import time
from typing import List

from src.base91x import base91x

LEN = 100
SIZE = 1 << 18


def perf_test() -> int:
    encoding_stat: List[float] = []
    encoding_average: float = 0
    encoding_summa: float = 0
    encoding_sigma: float = 0

    decoding_stat: List[float] = []
    decoding_average: float = 0
    decoding_summa: float = 0
    decoding_sigma: float = 0

    for n in range(LEN):
        data = random.randbytes(SIZE)
        start_time = time.time()
        text = base91x.encode(data)
        encoding_stop_time = time.time()
        refurbish_data = base91x.decode(text)
        decoding_stop_time = time.time()
        assert data == refurbish_data
        encoding_elapsed_time = encoding_stop_time - start_time
        encoding_summa += encoding_elapsed_time
        encoding_stat.append(encoding_elapsed_time)
        decoding_elapsed_time = decoding_stop_time - encoding_stop_time
        decoding_summa += decoding_elapsed_time
        decoding_stat.append(decoding_elapsed_time)

    encoding_average = encoding_summa / LEN
    for i in encoding_stat:
        encoding_sigma += (encoding_average - i) ** 2
    encoding_sigma /= LEN
    encoding_sigma = math.sqrt(encoding_sigma)
    print(f"ENCODING Average = {encoding_average} Deviation = {encoding_sigma}")

    decoding_average = decoding_summa / LEN
    for i in decoding_stat:
        decoding_sigma += (decoding_average - i) ** 2
    decoding_sigma /= LEN
    decoding_sigma = math.sqrt(decoding_sigma)
    print(f"DECODING Average = {decoding_average} Deviation = {decoding_sigma}")

    return 0


def main() -> int:
    start_time = time.time()
    perf_test()
    print(f"Total time: {time.time() - start_time} SIZE={SIZE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

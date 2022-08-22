import math
import random
import sys
import time
from typing import List

import base91

LEN = 100
SIZE = 1 << 22


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
        text = base91.encode(data)
        encoding_stop_time = time.time()
        refurbish_data = base91.decode(text)
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


assert 3 == sys.version_info.major and 9 <= sys.version_info.minor

if "__main__" == __name__:
    sys.exit(main())

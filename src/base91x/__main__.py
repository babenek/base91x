"""Base91x encoder-decoder
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
import sys

from base91x import base91x


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main() -> int:
    """main function

    Args:
        sys.argv[1]: -e|-d
        sys.argv[2]: input file
        sys.argv[3]: output file
    Return:
        EXIT_SUCCESS if no exception was thrown
    """
    result = 1
    if 4 == len(sys.argv):
        if '-e' == sys.argv[1]:
            with open(sys.argv[2], 'rb') as in_file:
                with open(sys.argv[3], 'wt', encoding='ascii') as out_file:
                    out_file.write(base91x.encode(in_file.read()))
                    result = 0
        elif '-d' == sys.argv[1]:
            with open(sys.argv[2], 'rt', encoding='ascii', errors='ignore') as in_file:
                with open(sys.argv[3], 'wb') as out_file:
                    out_file.write(base91x.decode(in_file.read()))
                    result = 0

    if 0 != result:
        print("base91x -e|-d <in-file> <out-file>")
    return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == "__main__":
    sys.exit(main())

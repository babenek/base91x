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
import random
import string
from random import randbytes

from src.base91x import base91x

TEXT = "The quick brown\r\nfox\tjumps\nover\rthe lazy\n\rdog!"
PANGRAM = "Thequickbrownfoxjumpsoverthelazydog!"
DATA = [88, 136, 162, 112, 31, 156, 195, 75, 208, 5, 61, 106, 20, 163, 227, 172, 240, 150, 163, 100, 63, 170, 82,
        175, 58, 17, 203, 5, 3]


def test_static_alphabet():
    assert len(base91x.BASE91X_ALPHABET) == base91x.BASE91X_LEN


def test_static_decode():
    data = base91x.decode(TEXT)
    assert list(data) == DATA


def test_static_encode():
    text = base91x.encode(bytes(DATA))
    assert text == PANGRAM


def test_refurbish_small():
    for n in range(33):
        original_data = randbytes(n)
        text = base91x.encode(original_data)
        refurbish_data = base91x.decode(text)
        assert len(original_data) == len(refurbish_data)
        assert original_data == refurbish_data, text


def test_refurbish_large():
    original_data = randbytes(65536)
    text = base91x.encode(original_data)
    refurbish_data = base91x.decode(text)
    assert len(original_data) == len(refurbish_data)
    assert original_data == refurbish_data, text


def test_stress_full_decode():
    text = ""
    text_size = random.randint(0, 65536)
    while text_size > len(text):
        text += chr(random.randint(0, 0x10FFFF))
    assert len(text) == text_size
    data = base91x.decode(text)
    assert len(data) <= text_size


def test_stress_ascii_decode():
    text = ""
    text_size = random.randint(0, 65536)
    while text_size > len(text):
        text += random.choice(string.printable)
    assert len(text) == text_size
    data = base91x.decode(text)
    assert len(data) <= text_size

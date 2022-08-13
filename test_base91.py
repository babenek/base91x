import random
from random import randbytes

import base91

TEXT = "The quick brown\r\nfox\tjumps\nover\rthe lazy\n\rdog!"
PANGRAM = "Thequickbrownfoxjumpsoverthelazydog!"
DATA = [88, 136, 162, 112, 31, 156, 195, 75, 208, 5, 61, 106, 20, 163, 227, 172, 240, 150, 163, 100, 63, 170, 82,
        175, 58, 17, 203, 5, 3]


def test_static_alphabet():
    assert len(base91.alphabet) == base91.base


def test_static_decode():
    data = base91.decode(TEXT)
    assert list(data) == DATA


def test_static_encode():
    text = base91.encode(bytes(DATA))
    assert text == PANGRAM


def test_refurbish_small():
    for n in range(33):
        original_data = randbytes(n)
        text = base91.encode(original_data)
        refurbish_data = base91.decode(text)
        assert len(original_data) == len(refurbish_data)
        assert original_data == refurbish_data, text


def test_refurbish_large():
    original_data = randbytes(65536)
    text = base91.encode(original_data)
    refurbish_data = base91.decode(text)
    assert len(original_data) == len(refurbish_data)
    assert original_data == refurbish_data, text


def test_stress_decode():
    text = ""
    text_size = random.randint(0, 65536)
    while text_size > len(text):
        text += chr(random.randint(0, 0x10FFFF))
    assert len(text) == text_size
    data = base91.decode(text)
    assert len(data) <= text_size

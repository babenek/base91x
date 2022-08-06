import unittest
from random import randbytes

import base91


class Base91Test(unittest.TestCase):
    TEXT = "The quick brown\r\nfox\tjumps\nover\rthe lazy\n\rdog!"
    PANGRAM = "Thequickbrownfoxjumpsoverthelazydog!"
    DATA = [88, 136, 162, 112, 31, 156, 195, 75, 208, 5, 61, 106, 20, 163, 227, 172, 240, 150, 163, 100, 63, 170, 82,
            175, 58, 17, 203, 5, 3]

    def test_static_decode(self):
        data = base91.decode(self.TEXT)
        self.assertEqual(self.DATA, list(data))

    def test_static_encode(self):
        text = base91.encode(bytes(self.DATA))
        self.assertEqual(self.PANGRAM, text)

    def test_refurbish_small(self):
        for n in range(33):
            original_data = randbytes(n)
            text = base91.encode(original_data)
            refurbish_data = base91.decode(text)
            self.assertEqual(original_data, refurbish_data, text)

    def test_refurbish_large(self):
        original_data = randbytes(65536)
        text = base91.encode(original_data)
        refurbish_data = base91.decode(text)
        self.assertEqual(original_data, refurbish_data, text)

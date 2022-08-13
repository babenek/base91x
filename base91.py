"""
MIT License

Copyright (c) 2022 Roman Babenko

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

# Base of the numeric system is 91 dec equals ASCII symbol [
base = ord('[')

# Bits in one byte. Should be 8
char_bit = 8

# Pair of base91 symbols might code 13 bits
b91word_bit = 13

# 8192 possibly values for 13 bits
b91word_size = 0x2000

# Mask for 13 bits
b91word_mask = 0x1FFF

HI: bytes = \
    b"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" \
    b"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" \
    b"}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}" \
    b"|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||" \
    b"{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{" \
    b"zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz" \
    b"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy" \
    b"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
    b"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww" \
    b"vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv" \
    b"uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu" \
    b"ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt" \
    b"sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss" \
    b"rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr" \
    b"qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" \
    b"ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp" \
    b"ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo" \
    b"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn" \
    b"mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm" \
    b"lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll" \
    b"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" \
    b"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj" \
    b"iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii" \
    b"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh" \
    b"ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg" \
    b"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff" \
    b"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" \
    b"ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd" \
    b"ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc" \
    b"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" \
    b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
    b"```````````````````````````````````````````````````````````````````````````````````````````" \
    b"___________________________________________________________________________________________" \
    b"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" \
    b"]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]" \
    b"###########################################################################################" \
    b"[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[" \
    b"ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ" \
    b"YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY" \
    b"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
    b"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" \
    b"VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" \
    b"UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU" \
    b"TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT" \
    b"SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS" \
    b"RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR" \
    b"QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ" \
    b"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP" \
    b"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO" \
    b"NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN" \
    b"MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM" \
    b"LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL" \
    b"KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK" \
    b"JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ" \
    b"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII" \
    b"HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH" \
    b"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG" \
    b"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF" \
    b"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" \
    b"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD" \
    b"CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC" \
    b"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" \
    b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
    b"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" \
    b"???????????????????????????????????????????????????????????????????????????????????????????" \
    b">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
    b"===========================================================================================" \
    b"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" \
    b";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;" \
    b":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" \
    b"9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999" \
    b"8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888" \
    b"7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777" \
    b"6666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666" \
    b"5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555" \
    b"4444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444" \
    b"3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333" \
    b"2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222" \
    b"1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" \
    b"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000" \
    b"///////////////////////////////////////////////////////////////////////////////////////////" \
    b"..........................................................................................." \
    b"-------------------------------------------------------------------------------------------" \
    b",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,," \
    b"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" \
    b"*******************************************************************************************" \
    b")))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))" \
    b"(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((" \
    b"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" \
    b"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" \
    b"%%"
LO: bytes = \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%" \
    b"!~"


def _decode_chunk(hi: int, lo: int) -> int:
    if 90 > hi:
        return base * hi + lo
    elif 90 == hi:
        if 0 == lo:
            return 8190
        elif 1 == lo:
            return 8191
    return -1


def _decode_symbol(a: str) -> int:
    x = ord(a)
    if 92 < x < 127 or 39 < x < 92 or 36 < x < 39:
        return 0x7F ^ x
    elif 33 == x:
        return 0
    elif 35 == x:
        return 35
    elif 36 == x:
        return 88
    else:
        return -1


def encode(data: bytes) -> str:
    """
    :param data:
    :return:
    """
    text = ""

    collector: int = 0
    bit_collected: int = 0
    for n in data:
        collector |= n << bit_collected
        bit_collected += char_bit
        while b91word_bit <= bit_collected:
            cod = b91word_mask & collector
            text += chr(LO[cod])
            text += chr(HI[cod])
            collector >>= b91word_bit
            bit_collected -= b91word_bit

    if 0 != bit_collected:
        cod = b91word_mask & collector
        text += chr(LO[cod])
        if 7 <= bit_collected:
            text += chr(HI[cod])
    return text


def decode(text: str) -> bytearray:
    """

    :param text:
    :return:
    """
    data = bytearray()
    collector: int = 0
    bit_collected: int = 0
    lower: int = -1
    for symbol in text:
        digit = _decode_symbol(symbol)
        if -1 == digit:
            continue
        if -1 == lower:
            lower = digit
            continue
        cod = _decode_chunk(digit, lower)
        if (b91word_mask & cod) != cod:
            lower = -1
            continue

        collector |= cod << bit_collected
        bit_collected += b91word_bit
        lower = -1

        while char_bit <= bit_collected:
            data.append(0xFF & collector)
            collector >>= char_bit
            bit_collected -= char_bit

    if -1 != lower:
        collector |= _decode_chunk(0, lower) << bit_collected
        bit_collected += (char_bit - 1)

    if char_bit <= bit_collected:
        data.append(0xFF & collector)

    return data


def main(argv) -> int:
    """main function
    argv[1]: -e|-d
    argv[2]: input file
    argv[3]: output file
    """
    result = 1
    if 4 == len(argv):
        if '-e' == argv[1]:
            with open(argv[2], 'rb') as in_file:
                with open(argv[3], 'wt', encoding='ascii') as out_file:
                    out_file.write(encode(in_file.read()))
                    result = 0
        elif '-d' == argv[1]:
            with open(argv[2], 'rt', encoding='ascii', errors='ignore') as in_file:
                with open(argv[3], 'wb') as out_file:
                    out_file.write(decode(in_file.read()))
                    result = 0

    if 0 != result:
        print("base91 -e|-d <in-file> <out-file>")
    return result


if "__main__" == __name__:
    sys.exit(main(sys.argv))

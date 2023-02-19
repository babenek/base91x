# base91x

This base91x method provides data encoding and decoding 
using numeric system of base 91 with specific alphabet that does not require
escaping any symbols in C, C++ (and many other languages?) string.
'x' - means the alphabet was obtained with XOR function.


The alphabet contains visible printable characters of ASCII except:

`"` Quotation mark

`'` Apostrophe

`\` Backslash

An encoded string might be used for JSON string if JSON does not require to escape / Slash.

Encoded string size ~ 16 * original size / 13.

There is possibility to extend the algorithm to use 89 codes during decode.

The alphabet transforms from base91 value with operation XOR(0x7F) with the tree exceptions.

The alphabet in the order:

```
!~}|{zyxwvutsrqponmlkjihgfedcba`_^]#[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)($&%
```

### PAY ATTENTION:
Encoded string may have awkwardly sequence ``/*`` or ``*/``
It may hurt C or C++ code when the string is placed into code.
But sequence %%% should not appear. So, encoded string might be placed with raw string literal:

char string[]=R"%%%( a string )%%%";

Workaround: use space | line feed | tab in encoded text to break wrong sequence due the algorithm skips non alphabet symbols.
e.g. ``Ma^7*/0629`` -> ``Ma^7* /0629``

The algorithm is not compatible with https://base91.sourceforge.net/

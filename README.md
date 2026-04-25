# base91x
https://pypi.org/project/base91x/


[![Test](https://github.com/babenek/base91x/actions/workflows/main.yml/badge.svg)](https://github.com/babenek/base91x/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/babenek/base91x/branch/main/graph/badge.svg)](https://codecov.io/gh/babenek/base91x)
[![GitHub release (latestSemVer)](https://img.shields.io/github/v/release/babenek/base91x)](https://github.com/babenek/base91x/releases)
[![PyPI](https://img.shields.io/pypi/v/base91x)](https://pypi.org/project/base91x/)
[![License](https://img.shields.io/badge/licence-MIT-green.svg?style=flat)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/base91x.svg)](https://badge.fury.io/py/base91x)

This base91x method provides data encoding and decoding
using numeric system of base 91 with specific alphabet that does not require
escaping any symbols in C, C++ (and many other languages?) string.
'x' - means the alphabet was obtained with XOR function.


The alphabet contains visible printable characters of ASCII except:

`"` Quotation mark

`'` Apostrophe

`\` Backslash

An encoded string might be used for JSON string if JSON does not require to escape ``/`` Slash.

Encoded string size ~ 16 * original size / 13.

There is possibility to extend the algorithm to use 89 codes during decode. (breaks compatibility)

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

HTML built-in encoding may hurt with ``</script>`` and so on, but it is almost impossible to appear the symbols from binary data.
Anyway - extra spaces do the workaround to fix parsing issue. ``< / script >`` is not valid closed tag.

The algorithm is not compatible with https://base91.sourceforge.net/

Current realization for:
- [Python](./src/base91x/base91x.py)
- [C](./src/base91x.c)
- [C++](./include/base91x.hpp) (header realization)
- [Java](./src/main/java/base91x/Base91x.java)
- [JS](./src/base91x.js)

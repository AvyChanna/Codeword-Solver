# Codeword Solver

**usage: cwsolver.py [-h] dictionary [patterns ...]**

Dictionary word solver

**positional arguments:**

*dictionary*  dictionary file location, support `txt`, `pickle` and `json` files

*patterns*    patterns to search

**optional arguments:**

*-h, --help*  show this help message and exit

Pattern must the string input that needs to be solved.
Use letters(a-z and A-Z) for known entries, digits(1-9) for same entries and a dot(.)
for unknown entries. For example, the pattern "1a1" prints all 3 letter words
which have same first and third letter, and the second entry is the letter `a`.

**caution:**

This script is not well optimized, this should not be a problem for modern
processors but if you are low on main memory, try using a smaller dictionary or make
a better one. This is also not the fastest, because of the algorithm.

**example:**

*(These results depend on the dictionary used, may differ for other users)*

```shell
$ /path/to/python3 cwsolver.py /path/to/dict "1dg."
edge edgy
$ /path/to/python3 cwsolver.py /path/to/dict "12121212121212"
[!] No results found
```

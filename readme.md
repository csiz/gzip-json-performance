Compare performance (speed and size) of gzip+json to an efficient binary representation of the data.

Size comparison
---------------

Compressed json vs binary for small numbers (around 1.0):

    json 3.29mb json/raw 43%
    binary 3.03mb binary/raw 40%
    json/binary 1.09

Compressed json vs binary for large numbers (around 1000000):

    json 2.58mb json/raw 34%
    binary 3.10mb binary/raw 41%
    json/binary 0.83

Compressed json vs binary for full precision doubles:

    json 8.90mb json/raw 117%
    binary 7.27mb binary/raw 95%
    json/binary 1.22

Compressed json vs binary for objects ({"small number", "large number", "choice"}):

    json 8.36mb json/raw 44%
    binary 6.59mb binary/raw 35%
    json/binary 1.27

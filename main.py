from __future__ import division, print_function, absolute_import
# Python 2.7, Numpy 1.7.1
################################################################################

import numpy as np
import zlib
import math
import array
import json

def round_sigfigs(numbers, sigfigs):
    """Round numbers to significant figures."""

    binary_mantissas, binary_exponents = np.frexp(numbers)
    decimal_exponents = math.log10(2) * binary_exponents
    int_exponents = np.floor(decimal_exponents)

    decimal_mantissas = binary_mantissas * 10 ** (decimal_exponents - int_exponents)

    return np.around(decimal_mantissas, decimals=sigfigs-1) * 10**int_exponents

def natural_numbers(n, magnitude=1.0):
    """Get rounded numbers from an exponential distribution."""
    numbers = np.random.exponential(size=n) * magnitude
    round_numbers = round_sigfigs(numbers, sigfigs=4)
    return list(round_numbers)

def mb_size(s):
    return len(s)/(1024**2)

def test_numbers(n=1e6):
    small = natural_numbers(n, 1.0)
    large = natural_numbers(n, 1e6)

    small_raw = mb_size(array.array("d", small).tostring())
    large_raw = mb_size(array.array("d", large).tostring())
    small_binary = mb_size(zlib.compress(array.array("d", small).tostring()))
    large_binary = mb_size(zlib.compress(array.array("d", large).tostring()))
    small_json = mb_size(zlib.compress(json.dumps(small)))
    large_json = mb_size(zlib.compress(json.dumps(large)))
    
    print("""
        Compressed json vs binary for small numbers (around 1.0):
            json {:.2f}mb json/raw {:.0f}%
            binary {:.2f}mb binary/raw {:.0f}%
            json/binary {:.2f}
        """.format(
            small_json, small_json/small_raw*100, 
            small_binary, small_binary/small_raw*100,
            small_json/small_binary
        )
    )

    print("""
        Compressed json vs binary for large numbers (around 1000000):
            json {:.2f}mb json/raw {:.0f}%
            binary {:.2f}mb binary/raw {:.0f}%
            json/binary {:.2f}
        """.format(
            large_json, large_json/large_raw*100, 
            large_binary, large_binary/large_raw*100,
            large_json/large_binary
        )
    )

def test_objects(n=1e6):
    small = natural_numbers(n, 1.0)
    large = natural_numbers(n, 1e6)
    enum = ["zero", "one", "two", "three", "four"]
    choices_int = map(int, np.random.choice(range(len(enum)), size=n))
    choices_str = [enum[i] for i in choices_int]

    binary_repr = \
        "size\n{}\n" \
        "small number\n{}\n" \
        "large number\n{}\n" \
        "choice\n{}\n"

    binary_raw = binary_repr.format(
        n, 
        array.array("d", small).tostring(), 
        array.array("d", large).tostring(),
        array.array("i", choices_int).tostring())

    binary_compressed = mb_size(zlib.compress(binary_raw))
    binary_raw = mb_size(binary_raw)

    json_repr = [
        {"small number": s, "large number": l, "choice": c}
        for s, l, c in zip(small, large, choices_str)
    ]

    json_raw = json.dumps(json_repr)
    json_compressed = mb_size(zlib.compress(json_raw))

    print("""
        Compressed json vs binary for objects:
            json {:.2f}mb json/raw {:.0f}%
            binary {:.2f}mb binary/raw {:.0f}%
            json/binary {:.2f}
        """.format(
            json_compressed, json_compressed/binary_raw*100, 
            binary_compressed, binary_compressed/binary_raw*100,
            json_compressed/binary_compressed
        )
    )

def main():
    test_numbers()
    test_objects()

if __name__ == "__main__":
    main()

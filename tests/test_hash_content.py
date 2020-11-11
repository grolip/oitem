#!/usr/bin/env python3
from pathlib import Path

from oitem import HashContent

HOME = Path(__file__).parent.joinpath("home")

def test_hash():
    target = str(HOME.joinpath('file1.txt'))
    target2 = str(HOME.joinpath('other/ofile1.txt'))
    item_col = HashContent([target, target2])
    result = [ (item, digest) for (item, digest) in item_col.collect() ]

    assert len(result) == 2
    assert result[0][1] == result[1][1]

def test_bad_alg():
    target = str(HOME.joinpath('*'))

    try:
        item_col = HashContent([target], algorithm = "__bad_alg")
        result = [ (item, digest) for (item, digest) in item_col.collect() ]
    except ValueError:
        result = None

    assert result == None
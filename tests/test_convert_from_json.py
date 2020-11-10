#!/usr/bin/env python3
from pathlib import Path

from oitem import ConvertFromJson

HOME = Path(__file__).parent.joinpath("home")

def test_read_all_json():
    target = str(HOME)
    item_col = ConvertFromJson([target], recurse = True)
    result = [ item for (item, data) in item_col.collect() ]

    assert len(result) != 0
    assert HOME.joinpath("file1.json") in result
    assert HOME.joinpath("other/ofile1.json") in result
    assert HOME.joinpath("file1.txt") not in result

def test_encoding():
    target = str(HOME.joinpath('*'))
    item_col = ConvertFromJson([target], encoding = "ascii")
    result = [ item for (item, data) in item_col.collect() ]

    assert HOME.joinpath("file2.json") in result
    assert HOME.joinpath("file1.json") not in result

def test_bad_include():
    target = str(HOME.joinpath('*'))
    item_col = ConvertFromJson([target], include = ["*.txt"])
    result = [ item for item in item_col.collect() ]

    assert len(result) == 0
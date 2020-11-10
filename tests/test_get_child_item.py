#!/usr/bin/env python3
from pathlib import Path

from oitem import GetChildItem

HOME = Path(__file__).parent.joinpath("home")

def test_wildcard():
    target = str(HOME.joinpath('*'))
    item_col = GetChildItem([target])
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('other/other2') in result
    assert HOME.joinpath('other') not in result
    assert HOME.joinpath('file1.txt') not in result

def test_recurse():
    target = str(HOME)
    item_col = GetChildItem([target], recurse = True)
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('other') in result
    assert HOME.joinpath('other/other2/ofile1.txt') in result
    assert HOME not in result

def test_recurse_with_depth():
    target = str(HOME)
    item_col = GetChildItem([target], recurse = True, depth = 2)
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('other/other2') in result
    assert HOME.joinpath('other/other2/ofile1.txt') in result
    assert HOME not in result

def test_exclude_md():
    target = str(HOME)
    item_col = GetChildItem([target], exclude = ["*.md"])
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('other') in result
    assert HOME.joinpath('file1.md') not in result

def test_include_txt():
    target = str(HOME)
    item_col = GetChildItem([target], include = ["*.txt"])
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('file3.txt') in result
    assert HOME.joinpath('other') not in result
    assert HOME.joinpath('file1.md') not in result

def test_ignore_dir():
    target = str(HOME)
    item_col = GetChildItem([target], ignore_dir = True)
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('file3.txt') in result
    assert HOME.joinpath('file1.md') in result
    assert HOME.joinpath('other') not in result

def test_ignore_file():
    target = str(HOME)
    item_col = GetChildItem([target], ignore_file = True)
    result = [ item for item in item_col.collect() ]

    assert HOME.joinpath('other') in result
    assert HOME.joinpath('file3.txt') not in result
    assert HOME.joinpath('file1.md') not in result
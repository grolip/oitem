#!/usr/bin/env python3
from pathlib import Path

from oitem import GetContent

HOME = Path(__file__).parent.joinpath("home")

def test_read_all_lines():
    target = str(HOME.joinpath('other/other2/ofile6.txt'))
    item_col = GetContent([target])
    result = [ content for (item, content) in item_col.collect() ]

    assert len(result) == 1
    assert result[0][32].startswith('33:')

def test_read_several_lines():
    target = str(HOME.joinpath('other/other2/ofile6.txt'))
    item_col = GetContent([target], nlines = 8)
    result = [ content for (item, content) in item_col.collect() ]

    assert len(result) == 1
    assert len(result[0]) == 8
    assert result[0][-1].startswith('8:')

def test_read_last_lines():
    target = str(HOME.joinpath('other/other2/ofile6.txt'))
    item_col = GetContent([target], reverse = True)
    result = [ content for (item, content) in item_col.collect() ]

    assert len(result) == 1
    assert result[0][1].startswith('40:')

def test_other_delimiter():
    target = str(HOME.joinpath('other/other2/ofile6.txt'))
    item_col = GetContent([target], nlines = 8, delimiter = 'b')
    result = [ content for (item, content) in item_col.collect() ]

    assert len(result) == 1
    assert len(result[0]) == 8
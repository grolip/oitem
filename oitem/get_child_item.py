#!/usr/bin/env python3
from typing import Set

from .get_item import AnyPath, GetItem

class GetChildItem(GetItem):
    def get_path_list(self) -> Set[AnyPath]:
        matches = set()

        for path in super().get_path_list():
            if path.is_dir():
                matches.update(path.iterdir())
        return matches

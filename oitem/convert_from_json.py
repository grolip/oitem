#!/usr/bin/env python3
import json
from typing import Any, Dict, Iterator, List, Tuple

from .get_item import AnyPath, GetItem

class ConvertFromJson(GetItem):
    def __init__(self, 
                path: List[str], 
                encoding: str = "utf8",
                include: List[str] = ["*.json"],
                *args, 
                **kwargs):
        super().__init__(path, include = include, *args, **kwargs)
        self.encoding = encoding
        self.ignore_dir = True

    def collect(self) -> Iterator[Tuple[AnyPath, Dict[str, Any]]]:
        for path in super().collect():
            try:
                data = json.loads(path.read_text(encoding = self.encoding))
                yield (path, data)
            except (PermissionError, UnicodeDecodeError, json.JSONDecodeError):
                pass
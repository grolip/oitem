#!/usr/bin/env python3
import hashlib
from typing import Iterator, List, Set, Tuple

from .get_item import AnyPath, GetItem

class HashContent(GetItem):
    def __init__(self, 
                path: List[str], 
                algorithm: str = "sha256",
                *args, 
                **kwargs):
        super().__init__(path, *args, **kwargs)
        self.algorithm = algorithm
        self.ignore_dir = True

    @classmethod
    def algorithms_available(self) -> Set[str]:
        """Alias pour hashlib.algorithms_available"""
        return hashlib.algorithms_available

    def get_block_size(self, path: AnyPath) -> int:
        """Connaître la taille maximale de données à lire en une fois"""
        return getattr(path.stat(), "blk_size", 4096)

    def read_blocks(self, path: AnyPath) -> Iterator[bytes]:
        """Lire un fichier block par block pour préserver la mémoire"""
        block_size = self.get_block_size(path)
        data_size = -1

        with path.open("rb") as fd:
            while data_size != 0:
                data = fd.read(block_size)
                data_size = len(data)
                yield data
 
    def collect(self) -> Iterator[Tuple[AnyPath, str]]:
        for path in super().collect():
            hash_obj = hashlib.new(self.algorithm)

            for block in self.read_blocks(path):
                hash_obj.update(block)
            yield (path, hash_obj.hexdigest())

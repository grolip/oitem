#!/usr/bin/env python3
from fnmatch import fnmatch
from glob import glob
from pathlib import Path, PosixPath, WindowsPath
from typing import Iterator, List, Set, TypeVar

__all__ = ["ItemCollector", "GetItem"]

AnyPath = TypeVar('AnyPath', PosixPath, WindowsPath)

class ItemCollector:
    """Obtenir un ou plusieurs items"""
    def __init__(self,
            path: List[str],
            recurse: bool = False,
            depth: int = -1,
            follow_symlink: bool = False):
        self.path = path
        self.recurse = recurse
        self.depth = depth
        self.follow_symlink = follow_symlink

    def translate_path(self, path: str) -> AnyPath:
        """Convertir chaine de caractère en chemin absolue"""
        return Path(path).expanduser().resolve()

    def get_path_list(self) -> Set[AnyPath]:
        """Traduire les chemins en prenant en compte les wildcards"""
        matches = set()

        for path in self.path:
            for elem in glob(str(self.translate_path(path))):
                matches.add(Path(elem))
        return matches

    def iterdir_recursively(self, path: AnyPath, depth: int) -> Iterator[AnyPath]:
        """Renvoyer le contenu d'un dossier en l'explorant de manière récursive"""
        if self.depth == depth:
            return
        try:
            for child in path.iterdir():
                yield child

                if child.is_dir():
                    if not self.follow_symlink and child.is_symlink():
                        continue
                    yield from self.iterdir_recursively(child, depth + 1)
        except PermissionError:
            pass

    def collect(self) -> Iterator[AnyPath]:
        for path in self.get_path_list():
            yield path

            if path.is_dir() and self.recurse:
                yield from self.iterdir_recursively(path, 0)


class GetItem(ItemCollector):
    """Obtenir un ou plusieurs items avec des options de base de filtrage"""
    def __init__(self,
            path: List[str],
            include: List[str] = [],
            exclude: List[str] = [],
            ignore_dir: bool = False,
            ignore_file: bool = False,
            *args,
            **kwargs):
        super().__init__(path, *args, **kwargs)
        self.include = include
        self.exclude = exclude
        self.ignore_dir = ignore_dir
        self.ignore_file = ignore_file

    def is_included(self, path: AnyPath) -> bool:
        """Savoir si le nom du chemin respecte les règles d'inclusion"""
        if not self.include:
            return True

        for pattern in self.include:
            if fnmatch(path.name, pattern):
                return True
        return False

    def is_excluded(self, path: AnyPath) -> bool:
        """Savoir si le nom du chemin respecte les règles d'exclusion"""
        if not self.exclude:
            return False
        
        for pattern in self.exclude:
            if fnmatch(path.name, pattern):
                return True
        return False

    def collect(self) -> Iterator[AnyPath]:
        for path in super().collect():
            if self.is_excluded(path) or not self.is_included(path):
                continue

            if self.ignore_file and path.is_file():
                continue
            elif self.ignore_dir and path.is_dir():
                continue
            yield path

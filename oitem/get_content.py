#!/usr/bin/env python3
from typing import Iterator, List, Tuple

from .get_item import AnyPath, GetItem

def get_block_size(path: AnyPath) -> int:
    """Connaître la taille maximale de données à lire en une fois"""
    return getattr(path.stat(), "blk_size", 4096)


class GetContent(GetItem):
    def __init__(self, 
                path: List[str],
                encoding: str = "utf8",
                nlines: int = -1,
                delimiter: str = '\n',
                raw: bool = False,
                reverse: bool = False,
                *args, 
                **kwargs):
        super().__init__(path, *args, **kwargs)
        self.encoding = encoding
        self.nlines = nlines
        self.delimiter = delimiter
        self.raw = raw
        self.reverse = reverse
        self.ignore_dir = True

    def read_content(self, path: AnyPath) -> List[str]:
        """Lire le contenu comme une seul et unique ligne"""
        return [path.read_text(encoding = self.encoding)]

    def read_lines(self, path: AnyPath) -> List[str]:
        """Lire le contenu et le découper en lignes"""
        block_size = get_block_size(path)
        buffer = ""
        lines = []

        with path.open("r", encoding = self.encoding) as fd:
            while True:
                data = fd.read(block_size)

                if not data:
                    if buffer:
                        lines.append(buffer)
                    break

                data_delimited = data.split(self.delimiter)
                
                if len(data_delimited) > 1:
                    lines.append(buffer + data_delimited[0])
                    buffer = data_delimited[-1]
                    del data_delimited[-1]
                    del data_delimited[0]
                    lines += data_delimited
                else:
                    buffer += data

                if self.nlines != -1 and len(lines) >= self.nlines:
                    lines = lines[:self.nlines]
                    break
        return lines

    def read_last_lines(self, path: AnyPath) -> List[str]:
        """Lire le contenu par la fin et le découper en lignes"""
        block_size = get_block_size(path)
        buffer = ""
        lines = []

        with path.open("r", encoding = self.encoding) as fd:
            end_pos = fd.seek(0, 2)

            if end_pos - block_size > 0:
                fd.seek(end_pos - block_size)
            else:
                fd.seek(0)

            while True:
                cur_pos = fd.tell()
                data = fd.read(block_size)                
                data_delimited = list(reversed(data.split(self.delimiter)))

                if len(data_delimited) > 1:
                    lines.append(buffer + data_delimited[0])
                    buffer = data_delimited[-1]
                    del data_delimited[-1]
                    del data_delimited[0]
                    lines += data_delimited
                else:
                    buffer += data

                if self.nlines != -1 and len(lines) >= self.nlines:
                    lines = lines[:self.nlines]
                    break

                if cur_pos == 0:
                    if buffer:
                        lines.append(buffer)
                    break
                elif cur_pos - block_size < 0:
                    block_size = cur_pos
                    fd.seek(0)
                else:
                    fd.seek(cur_pos - block_size)
        return lines

    def collect(self) -> Iterator[Tuple[AnyPath, List[str]]]:
        if self.raw:
            read_lines = self.read_content
        elif self.reverse:
            read_lines = self.read_last_lines
        else:
            read_lines = self.read_lines

        for path in super().collect():
            try:
                yield (path, read_lines(path))
            except (PermissionError, UnicodeDecodeError):
                pass
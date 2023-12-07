from pathlib import Path
from typing import List


def load_per_line(file: Path, transform=str):
    with file.open() as f:
        for line in f:
            # if transform:
            #     yield transform()
            yield transform(line.strip("\n"))

def load_per_newline_block(file: Path, transform=str):
    with file.open() as f:
        block = ""
        for line in f:
            if line == "\n":
                yield block
                block = ""
            else:
                block += line

        yield block



def load_grid(file: Path) -> List[List[str]]:
    grid = []
    with file.open() as f:
        for line in f:
            grid.append([*line.rstrip()])

    return grid

from pathlib import Path

def load_per_line(file: Path, transform = str):
    with file.open() as f:
        for line in f:
            # if transform:
            #     yield transform()
            yield transform(line.strip("\n"))

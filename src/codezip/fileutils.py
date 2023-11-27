"""codezip.fileutils"""

from typing import TYPE_CHECKING
from pathlib import Path
import os

if TYPE_CHECKING:
    from typing import Callable, Pathlike, Generator


def get_matching_files(
    rootdir: "Pathlike", filter_fn: "Callable[[Pathlike], bool]"
) -> "Generator[Path, None, None]":
    """Yield all files in a directory matching a filter function."""

    if not os.path.isdir(rootdir):
        raise ValueError(f"{rootdir} is not a directory")

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for d in dirs:
            full_dir_path = Path(root) / d
            if filter_fn(full_dir_path):
                yield full_dir_path
            else:
                del dirs[dirs.index(d)]

        for f in files:
            full_file_path = Path(root) / f
            if filter_fn(full_file_path):
                yield full_file_path

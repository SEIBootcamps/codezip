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
        for i, d in enumerate([Path(root) / _d for _d in dirs]):
            if filter_fn(d):
                yield d
            else:
                del dirs[i]

        for f in [Path(root) / _f for _f in files]:
            if filter_fn(f):
                yield f

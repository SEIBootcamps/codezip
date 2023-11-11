"""codezip

Create .zip archives of lecture demos, starter code for lab exercises, etc.
"""

from typing import TYPE_CHECKING
from pathlib import Path
from zipfile import ZipFile
import os

import igittigitt

from . import gitutils

if TYPE_CHECKING:
    from typing import Callable, Pathlike, Generator

ignore_parser = igittigitt.IgnoreParser()


def zip_code(
    zip_name: str, target_dir: "Pathlike", ignore_file: "Pathlike" = ".codezipignore"
) -> None:
    """Use this to archive code for students to download."""

    ignore_parser.parse_rule_files(base_dir=target_dir, filename=ignore_file)
    ignore_parser.add_rule(".codezipignore", base_path=target_dir)

    is_git_repo = gitutils.is_git_repo(target_dir)

    def filter_files(file: Path) -> bool:
        """Filter out files that ignored by .gitignore or .codezipignore."""

        gitignored = False
        if is_git_repo:
            gitignored = gitutils.is_ignored_by_git(file, cwd=target_dir)

        return not gitignored and not ignore_parser.match(file)

    with ZipFile(zip_name, "w") as zfile:
        for f in _get_matching_files(target_dir, filter_files):
            print(f)
            zfile.write(f.resolve(), f.relative_to(target_dir))


def _get_matching_files(
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

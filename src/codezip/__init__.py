"""codezip

Create .zip archives of lecture demos, starter code for lab exercises, etc.
"""

from typing import TYPE_CHECKING
from pathlib import Path
from zipfile import ZipFile

from . import gitutils, fileutils, ignoreparser

if TYPE_CHECKING:
    from typing import Pathlike, Optional, List

ignore_parser = ignoreparser.create_ignore_parser()


def zip_code(
    zip_name: str,
    target_dir: "Pathlike",
    ignore_file: "Pathlike" = ".codezipignore",
    additional_ignore_patterns: "Optional[List[str]]" = None,
) -> None:
    """Use this to archive code for students to download."""

    ignoreparser.init_ignore_parser(
        ignore_parser, target_dir, ignore_file, additional_ignore_patterns
    )

    is_git_repo = gitutils.is_git_repo(target_dir)

    def filter_files(file: Path) -> bool:
        """Filter out files that ignored by .gitignore or .codezipignore."""

        gitignored = False
        if is_git_repo:
            gitignored = gitutils.is_ignored_by_git(file, cwd=target_dir)

        return not gitignored and not ignore_parser.match(file)

    with ZipFile(zip_name, "w") as zfile:
        for f in fileutils.get_matching_files(target_dir, filter_files):
            zfile.write(f.resolve(), f.relative_to(target_dir))

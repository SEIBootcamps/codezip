from typing import TYPE_CHECKING
import igittigitt

from . import gitutils

if TYPE_CHECKING:
    from typing import Pathlike, Optional, List


IGNORE_FILE_NAME = ".codezipignore"


def create_ignore_parser() -> "igittigitt.IgnoreParser":
    """Create a new IgnoreParser instance."""

    return igittigitt.IgnoreParser()


def init_ignore_parser(
    ignore_parser: "igittigitt.IgnoreParser",
    target_dir: "Pathlike",
    ignore_file: "Pathlike" = IGNORE_FILE_NAME,
    additional_ignore_patterns: "Optional[List[str]]" = None,
) -> None:
    """Initialize an IgnoreParser instance."""

    if gitutils.is_git_repo(target_dir):
        repo_base = gitutils.get_repo_base_dir(target_dir)
        ignore_parser.parse_rule_files(repo_base, ignore_file)

    ignore_parser.add_rule(ignore_file, base_path=target_dir)
    if additional_ignore_patterns:
        for pattern in additional_ignore_patterns:
            ignore_parser.add_rule(pattern, base_path=target_dir)

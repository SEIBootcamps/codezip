from typing import TYPE_CHECKING
import igittigitt

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

    ignore_parser.parse_rule_files(base_dir=target_dir, filename=ignore_file)
    ignore_parser.add_rule(ignore_file, base_path=target_dir)
    if additional_ignore_patterns:
        for pattern in additional_ignore_patterns:
            ignore_parser.add_rule(pattern, base_path=target_dir)

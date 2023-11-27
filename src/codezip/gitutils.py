from typing import TYPE_CHECKING
import subprocess

if TYPE_CHECKING:
    from typing import Optional, Pathlike


def is_git_repo(path: "Pathlike") -> bool:
    """Check if a path is a Git repository."""

    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=path)
    except subprocess.CalledProcessError:
        return False

    return True


def get_repo_base_dir(path: "Pathlike") -> "Optional[Pathlike]":
    """Get the base directory of a Git repository."""

    try:
        base_dir = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=path
        )
    except subprocess.CalledProcessError:
        return None

    return base_dir.decode("utf-8").strip()


def is_ignored_by_git(file: "Pathlike", cwd: "Optional[Pathlike]" = None) -> bool:
    """Check if a file is ignored by Git."""

    try:
        subprocess.check_output(["git", "check-ignore", str(file)], cwd=cwd)
    except subprocess.CalledProcessError:
        return False

    return True

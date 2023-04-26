from typing import Generator, Optional
from pathlib import Path
import subprocess
import os


def tracked_files(rootdir: Path) -> Generator[Path, None, None]:
    """Yield all files tracked by Git in a directory."""

    if not os.path.isdir(rootdir):
        raise ValueError(f"{rootdir} is not a directory")

    if not is_git_repo(rootdir):
        raise ValueError(f"{rootdir} is not in a Git repository")

    for root, dirs, files in os.walk(rootdir, topdown=True):
        for i, d in enumerate(dirs):
            if is_ignored_by_git(Path(root) / d, cwd=rootdir):
                del dirs[i]
            else:
                yield Path(root) / d

        for name in files:
            filepath = Path(root) / name
            if not is_ignored_by_git(filepath, cwd=rootdir):
                yield filepath


def is_git_repo(path: Path) -> bool:
    """Check if a path is a Git repository."""

    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError:
        return False

    return True


def is_ignored_by_git(file: Path, cwd: Optional[Path] = None) -> bool:
    """Check if a file is ignored by Git."""

    try:
        subprocess.check_output(["git", "check-ignore", str(file)], cwd=cwd)
    except subprocess.CalledProcessError:
        return False

    return True

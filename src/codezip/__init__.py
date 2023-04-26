"""codezip

Create .zip archives of lecture demos, starter code for lab exercises, etc.
"""

from pathlib import Path
from zipfile import ZipFile
from . import gitutils


def zip_code(zip_name: str, target_dir: Path):
    """Use this to archive code for students to download."""

    with ZipFile(zip_name, "w") as zfile:
        for f in gitutils.tracked_files(target_dir):
            zfile.write(f.resolve(), f.relative_to(target_dir))

from pathlib import Path
from zipfile import ZipFile
import pytest

from codezip import zip_code


@pytest.fixture(scope="function")
def tests_dir() -> Path:
    """Return the path to the tests directory."""

    return Path(__file__).parent


def test_zip_code(tests_dir: Path) -> None:
    example_dir = tests_dir / "example"
    zip_to = example_dir / "example.zip"
    zip_code(zip_to, example_dir)

    with ZipFile(zip_to) as zfile:
        assert ".ignore_me/" not in zfile.namelist()
        assert ".ignore_me/ignore_me_too.txt" not in zfile.namelist()
        assert "include_me/but_ignore_me.txt" not in zfile.namelist()
        assert "ignore_this_file.txt" not in zfile.namelist()

        assert "include_me/" in zfile.namelist()
        assert "include_me/include_me_too.txt" in zfile.namelist()
        assert "include_me.txt" in zfile.namelist()

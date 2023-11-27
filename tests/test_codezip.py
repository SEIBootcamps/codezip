from pathlib import Path
from zipfile import ZipFile
import pytest

from codezip import zip_code


@pytest.fixture(scope="function")
def example_dir() -> Path:
    """Return the path to the tests/example directory."""

    return Path(__file__).parent / "example"


def test_zip_code(example_dir: Path) -> None:
    zip_to = example_dir / "example.zip"
    zip_code(zip_to, example_dir)

    with ZipFile(zip_to) as zfile:
        zipped_files = zfile.namelist()
        assert "_dont_include/" not in zipped_files
        assert "_dont_include/hello.txt" not in zipped_files
        assert ".ignore_me/" not in zipped_files
        assert ".ignore_me/ignore_me_too.txt" not in zipped_files
        assert "include_me/but_ignore_me.txt" not in zipped_files
        assert "ignore_this_file.txt" not in zipped_files

        assert "example/include_me/" in zipped_files
        assert "example/include_me.txt" in zipped_files
        assert "include_me/include_me_too.txt" in zipped_files
        assert "include_me.txt" in zipped_files
        assert "solution/hello.txt" in zipped_files


def test_additional_ignore_patterns(example_dir: Path) -> None:
    zip_to = example_dir / "example.zip"
    zip_code(zip_to, example_dir, additional_ignore_patterns=["solution"])

    with ZipFile(zip_to) as zfile:
        zipped_files = zfile.namelist()
        assert "_dont_include/" not in zipped_files
        assert "_dont_include/hello.txt" not in zipped_files
        assert ".ignore_me/" not in zipped_files
        assert ".ignore_me/ignore_me_too.txt" not in zipped_files
        assert "include_me/but_ignore_me.txt" not in zipped_files
        assert "ignore_this_file.txt" not in zipped_files
        assert "solution/" not in zipped_files
        assert "solution/hello.txt" not in zipped_files

        assert "example/include_me/" in zipped_files
        assert "example/include_me.txt" in zipped_files
        assert "include_me/include_me_too.txt" in zipped_files
        assert "include_me.txt" in zipped_files

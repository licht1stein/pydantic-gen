import shutil
from pathlib import Path

import pytest

from pydantic_gen import SchemaGen


@pytest.fixture
def example_yaml() -> Path:
    return Path(__file__).parent / "example.yml"


@pytest.fixture
def example_output():
    return (Path(__file__).parent / "example_output.py").read_text(encoding="utf-8")


@pytest.fixture
def example_generator(example_yaml):
    return SchemaGen(example_yaml.parent / "example.yml")


@pytest.fixture
def example_yaml_string(example_yaml) -> str:
    return example_yaml.read_text(encoding="utf8")


@pytest.fixture(scope="session")
def tmp_dir():
    tmp = Path(__file__).parent / "tmp"
    if not tmp.is_dir():
        tmp.mkdir()
    yield tmp
    shutil.rmtree(tmp)

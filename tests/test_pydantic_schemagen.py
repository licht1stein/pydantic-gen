import pytest

from pydantic_gen import SchemaGen


def test_make_module(example_output, example_generator):
    assert example_generator.code == example_output


def test_to_sys(example_generator):
    with pytest.raises(ModuleNotFoundError):
        from generated_output import GeneratedSchema1

    example_generator.to_sys("generated_output")
    from generated_output import GeneratedSchema1

    instance = GeneratedSchema1(id=1)
    assert instance.id == 1


def test_to_file(example_generator, example_output, tmp_dir):
    file = example_generator.to_file("./tmp/_result.py")
    assert file.is_file()
    assert file.read_text(encoding="utf8") == example_output


def test_init__file_not_found():
    with pytest.raises(FileNotFoundError):
        SchemaGen("foobar.yml")

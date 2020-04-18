# Pydantic Schemas Generator
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-gen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/pydantic-gen)](https://pypi.org/project/pydantic-gen/)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Flicht1stein%2Fpydantic-gen%2Fbadge&style=flat)](https://actions-badge.atrox.dev/licht1stein/pydantic-gen/goto)


## What this package does
This is a code generation package that converts YML definitions to Pydantic models (either python code or python objects).


## What is Pydantic 
[Pydantic](https://pydantic-docs.helpmanual.io/) is a python library for data validation and settings management using 
python type annotations.

Here's an [official example](https://pydantic-docs.helpmanual.io/#example) from the docs

## Why generate schemas?

Normally you just program the schemas within your program, but there are several 
use cases when code generation makes a lot of sense:

* You're programming several apps that use the same schema (think an API server 
and client library for it)
* You're programming in more than one programming language

## Getting started

### Installation

`pip install pydantic-gen`


### Usage

First you need to create a YAML file with your desired class schema. See 
[example.yml](./example.yml) file.

```python
from pydantic_gen import SchemaGen

generated = SchemaGen('example.yml')
```

The code is now generated and stored in `generated.code` attribute. There are 
two ways to use the code:

**1. Save it to a file, and use the file in your program.**

```python
generated.to_file('example_output.py')
```

You can inspect the resulting [example_output.py](./example_output.py)

**2. Import the generated classed directly without saving**

```python
generated.to_sys(module_name='generated_schemas')
```

After running `.to_sys()` module `'generated_schemas'` will be added to
`sys.modules` and become importable like a normal module:

```python
from generated_schemas import GeneratedSchema1

schema = GeneratedSchema1(id=1)
``` 

### Usage pattern

Recommended usage pattern is creating the yaml files needed for your projects
and storing them in a separate repository, to achieve maximum consistency across all projects.

### YAML-file structure

`schemas` - list of all schemas described

`name` - name of the generated class

`props` - list of properties of the class using python type 
annotation. Fields: `name` - field name, `type` - field type,
`optional` - bool, if True the type will be wrapped in `Optional`,
`default` - default value for the field.

`config` - list of config settings from [Model Config](https://pydantic-docs.helpmanual.io/usage/model_config/)
of pydantic.

### Testing

Project is fully covered by tests.

### Packaging notice
This project uses the excellent [poetry](https://python-poetry.org) for packaging. Please read about it and let's all start using
`pyproject.toml` files as a standard. Read more:

* [PEP 518 -- Specifying Minimum Build System Requirements for Python Projects](https://www.python.org/dev/peps/pep-0518/)

* [What the heck is pyproject.toml?](https://snarky.ca/what-the-heck-is-pyproject-toml/)

* [Clarifying PEP 518 (a.k.a. pyproject.toml)](https://snarky.ca/clarifying-pep-518/)



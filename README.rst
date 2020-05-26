==========================
Pydantic Schemas Generator
==========================
.. image:: https://img.shields.io/pypi/pyversions/pydantic-gen
    :target: https://pypi.org/project/pydantic-gen/
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. image:: https://img.shields.io/pypi/v/pydantic-gen
    :target: https://pypi.org/project/pydantic-gen/
.. image:: https://img.shields.io/pypi/dw/pydantic-gen
    :target: https://pypi.org/project/pydantic-gen/
.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Flicht1stein%2Fpydantic-gen%2Fbadge&style=flat
    :target: https://actions-badge.atrox.dev/licht1stein/pydantic-gen/goto
.. image:: https://readthedocs.org/projects/pydantic-gen/badge/?version=latest
    :target: https://pydantic-gen.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/badge/Support-With_coffee!-Green
    :target: https://www.buymeacoffee.com/licht1stein

----------------------
What this package does
----------------------
This is a code generation package that converts YML definitions to Pydantic models (either python code or python objects).

----------------
What is Pydantic
----------------
`Pydantic <https://pydantic-docs.helpmanual.io/>`_ is a python library for data validation and settings management using
python type annotations.

Take a look at the `official example <https://pydantic-docs.helpmanual.io/#example>`_ from the Pydantic docs.

---------------------
Why generate schemas?
---------------------
Normally you just program the schemas within your program, but there are several
use cases when code generation makes a lot of sense:

- You're programming several apps that use the same schema (think an API server and client library for it)

- You're programming in more than one programming language

---------------
Getting started
---------------

Installation
------------
Using pip:

.. code-block:: bash

    pip install pydantic-gen

Using `poetry <https://python-poetry.org/>`_:

.. code-block:: bash

    poetry add pydantic-gen

Usage
-----
First you need to create a YAML file with your desired class schema. See `example.yml <https://github.com/licht1stein/pydantic-gen/blob/documentation/example.yml>`_ file.

.. code-block:: python

    from pydantic_gen import SchemaGen

    generated = SchemaGen('example.yml')

The code is now generated and stored in `generated.code` attribute. There are
two ways to use the code:

1. Save it to a file, and use the file in your program:

.. code-block:: python

    generated.to_file('example_output.py')

You can inspect the resulting file in the `example_output.py <https://github.com/licht1stein/pydantic-gen/blob/documentation/example_output.py>`_

2. Or directly import the generated classed directly without saving:

.. code-block:: python

    generated.to_sys(module_name='generated_schemas')

After running `generated.to_sys(module_name='generated_schemas'` your generated code will be available for import:

.. code-block:: python

    import generated_schemas as gs

    schema = gs.GeneratedSchema1(id=1)

Usage pattern
-------------
Recommended usage pattern is creating the yaml files needed for your projects
and storing them in a separate repository, to achieve maximum consistency across all projects.

YAML-file structure
-------------------
`schemas` - list of all schemas described

`name` - name of the generated class

`props` - list of properties of the class using python type
annotation. Fields: `name` - field name, `type` - field type,
`optional` - bool, if True the type will be wrapped in `Optional`,
`default` - default value for the field.

`config` - list of config settings from `Model Config <https://pydantic-docs.helpmanual.io/usage/model_config/>`_
of pydantic.

Testing
-------
Project is fully covered by tests and uses pytest. To run:

.. code-block:: bash

    pytest

Packaging Notice
----------------
This project uses the excellent `poetry <https://python-poetry.org>`__ for packaging. Please read about it and let's all start using
`pyproject.toml` files as a standard. Read more:

* `PEP 518 -- Specifying Minimum Build System Requirements for Python Projects <https://www.python.org/dev/peps/pep-0518/>`_

* `What the heck is pyproject.toml? <https://snarky.ca/what-the-heck-is-pyproject-toml/>`_

* `Clarifying PEP 518 (a.k.a. pyproject.toml) <https://snarky.ca/clarifying-pep-518/>`_




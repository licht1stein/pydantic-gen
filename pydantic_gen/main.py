from __future__ import annotations

from pathlib import Path
from typing import Union, Dict, Optional

import attr
from box import Box
from jinja2 import Template

import black
from ruamel import yaml


def yaml_to_box(filename: Union[Path, str]) -> Box:
    """
    Takes a yaml file name and returns a Box dictionary.

    :param filename: Union[Path, str]
    :return: Box
    """
    filename = Path(filename)
    if not filename.is_file() and filename.parent != Path(__file__).parent:
        return yaml_to_box(Path(__file__).parent / filename.name)
    return Box(yaml.safe_load(filename.open("r", encoding="utf8")))


@attr.s
class SchemaGen:
    """
    Main class of the program that does all the work. Once the code is generated the output is stored in
    :class:`SchemaGen.code` property. You can choose to either save it to file with :class:`SchemaGen.to_file`
    or import to sys with :class:`SchemaGen.to_sys`

    Example usage:
    ::
        from pydantic_gen import SchemaGen

        generated = SchemaGen('example.yml')

    Once the code is generated you can save it to file:
    ::
        generated.to_file('generated_schemas.py')

    Or make it directly importable by adding to `sys.modules`:
    ::
        generated.to_sys(module_name='generated_schemas')

    After running `generated.to_sys(module_name='generated_schemas'` your code will be available for import:
    ::
        import generated_schemas as gs
    """

    filename: Optional[Union[Path, str, None]] = attr.ib(default=None)
    yaml_content: Dict = attr.ib(default=None)
    code: str = attr.ib(default=None)
    _additional_imports = set()

    _templates: Box = yaml_to_box("templates.yml")
    _module: Template = Template(_templates.module)
    _schemas: Template = Template(_templates.schemas)
    _schema: Template = Template(_templates.schema)
    _prop: Template = Template(_templates.prop)
    _config: Template = Template(_templates.config)

    def __attrs_post_init__(self):
        if not self.yaml_content:
            self._content_from_file()
        self.code = self._make_module_and_schemas()
        self.code = black.format_str(self.code, mode=black.FileMode())

    def _content_from_file(self):
        self.filename = Path(self.filename)
        if not self.filename.is_file():
            raise FileNotFoundError(f"{self.filename.name}")
        self.yaml_content = yaml_to_box(self.filename)

    @classmethod
    def from_string(cls, s: str) -> SchemaGen:
        """
        Generates code from a yaml string instead of file.

        :param s: yaml string
        :return: SchemaGen
        """
        d = yaml.safe_load(s)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d: dict) -> SchemaGen:
        """
        Alternative constructor. Takes a dict from reading a yaml file instead of the file itself and constructs a
        :class:`SchemaGen` object.

        :param d: dict
        :return: SchemaGen
        """
        return cls(yaml_content=Box(d))

    def _make_module_and_schemas(self) -> str:
        schemas = self._schemas.render(schemas=self._make_schemas())
        additional_imports = (
            "\n".join(sorted(list(self._additional_imports)))
            if self._additional_imports
            else ""
        )
        module = self._module.render(imports=additional_imports)
        return "\n\n\n".join([module, schemas])

    def _make_schemas(self) -> str:
        schemas = []
        for schema in self.yaml_content.schemas:
            schemas.append(self._make_schema(schema))
        return "\n\n\n".join(schemas)

    def _make_schema(self, schema: Box) -> str:
        props = [self._make_prop(prop) for prop in schema.props]
        config = self._make_config(schema.get("config"))
        config_text = "\n\n" + 4 * " " + config if config else ""
        props_text = "\n    ".join(props)
        return self._schema.render(
            name=schema.name, props=props_text, config=config_text
        )

    def _make_prop(self, prop: Box) -> str:
        if not prop.get("default"):
            default_value = ""
        elif prop.type in ["str", "date", "datetime", "time"]:
            default_value = f' = "{prop.default}"'
        else:
            default_value = f" = {prop.default}"

        if prop.type in ["date", "datetime", "time"]:
            self._additional_imports.add("import datetime as dt")
            prop.type = f"dt.{prop.type}"

        if prop.type == "uuid":
            self._additional_imports.add("import uuid")
            prop.type = "uuid.UUID"

        if prop.get("optional"):
            prop_type = f"Optional[{prop.type}]"
        else:
            prop_type = prop.type
        return self._prop.render(name=prop.name, type=prop_type, default=default_value)

    def _make_config(self, config: Box) -> str:
        if not config:
            return ""
        else:
            conf_text = ""
            for conf in config:
                conf_text += (
                    4 * " " + f"{list(conf.keys())[0]} = {list(conf.values())[0]}\n"
                )
        return self._config.render(confs=conf_text)

    def to_file(self, filename: Union[Path, str]) -> None:
        """
        Saves generated code to file.

        :param filename: Union[Path, str]
        :return: None
        """
        filename = Path(filename)
        filename.write_text(self.code, encoding="utf8")
        return filename

    def to_sys(self, module_name: str) -> None:
        """
        Saves generated code into sys.modules making the classes available for import.

        :param module_name: str : name of the module under which the code will be importable
        :return: None

        Example:
        ::
            from pydantic_gen import SchemaGen

            generated = SchemaGen('example.yml')
            generated.to_sys(module_name='generated_schemas')

        After running `generated.to_sys(module_name='generated_schemas'` your code will be available for import:
        ::
            import generated_schemas as gs
        """

        import sys
        from types import ModuleType

        mod = ModuleType(module_name)
        sys.modules[module_name] = mod
        exec(self.code, mod.__dict__)

    def print(self):
        """
        Prints the generated code.
        """
        print(self.code)

from pathlib import Path
from typing import Union

import attr
from box import Box
from jinja2 import Template

from ruamel import yaml


def yaml_to_box(filename: Union[Path, str]):
    filename = Path(filename)
    if not filename.is_file() and filename.parent != Path(__file__).parent:
        return yaml_to_box(Path(__file__).parent / filename.name)
    return Box(yaml.safe_load(filename.open("r", encoding="utf8")))


@attr.s
class SchemaGen:
    filename: Union[Path, str] = attr.ib()

    _templates: Box = yaml_to_box("templates.yml")
    _module: Template = Template(_templates.module)
    _schema: Template = Template(_templates.schema)
    _prop: Template = Template(_templates.prop)

    def __attrs_post_init__(self):
        self.filename = Path(self.filename)
        if not self.filename.is_file():
            raise FileNotFoundError(f"{self.filename.name}")
        self.file = yaml_to_box(self.filename)
        self.code = self._make_module()

    def _make_module(self):
        return self._module.render(schemas=self._make_schemas()) + "\n"

    def _make_schemas(self):
        schemas = []
        for schema in self.file.schemas:
            schemas.append(self._make_schema(schema))
        return "\n\n\n".join(schemas)

    def _make_schema(self, schema: Box):
        props = []
        for prop in schema.props:
            if not prop.get("default"):
                default_value = ""
            else:
                default_value = f" = {prop.default}"

            if prop.get("optional"):
                prop_type = f"Optional[{prop.type}]"
            else:
                prop_type = prop.type
            props.append(
                self._prop.render(name=prop.name, type=prop_type, default=default_value)
            )
        config = schema.get("config")
        if not config:
            conf_text = ""
        else:
            conf_text = "\n\n    class Config:\n"
            for conf in config:
                conf_text += (
                    f"        {list(conf.keys())[0]} = {list(conf.values())[0]}\n"
                )

        props_text = "\n    ".join(props)
        return self._schema.render(name=schema.name, props=props_text, config=conf_text)

    def to_file(self, filename: Union[Path, str]):
        filename = Path(filename)
        filename.write_text(self.code, encoding="utf8")

    def to_sys(self, module_name: str):
        import sys
        from types import ModuleType

        mod = ModuleType(module_name)
        sys.modules[module_name] = mod
        exec(self.code, mod.__dict__)

from pathlib import Path
from typing import Union

import attr
from box import Box
from jinja2 import Template

from ruamel import yaml


class PydanticSchemageException(Exception):
    pass


class GeneratedCodeExecutionFailed(PydanticSchemageException):
    pass


def yaml_to_box(filename: Union[Path, str]):
    filename = Path(filename)
    if not filename.is_file() and filename.parent != Path(__file__).parent:
        return yaml_to_box(Path(__file__).parent / filename.name)
    return Box(yaml.safe_load(filename.open("r", encoding="utf8")))


@attr.s
class SchemaGen:
    filename: Union[Path, str] = attr.ib()
    _additional_imports = set()

    _templates: Box = yaml_to_box("templates.yml")
    _module: Template = Template(_templates.module)
    _schemas: Template = Template(_templates.schemas)
    _schema: Template = Template(_templates.schema)
    _prop: Template = Template(_templates.prop)
    _config: Template = Template(_templates.config)

    def __attrs_post_init__(self):
        self.filename = Path(self.filename)
        if not self.filename.is_file():
            raise FileNotFoundError(f"{self.filename.name}")
        self.file = yaml_to_box(self.filename)
        self.code = self._make_module_and_schemas()


    def _make_module_and_schemas(self) -> str:
        schemas = self._schemas.render(schemas=self._make_schemas())
        additional_imports = (
            "\n".join(self._additional_imports) if self._additional_imports else ""
        )
        module = self._module.render(imports=additional_imports)
        return "\n\n\n".join([module, schemas])

    def _make_schemas(self) -> str:
        schemas = []
        for schema in self.file.schemas:
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

    def to_file(self, filename: Union[Path, str]):
        filename = Path(filename)
        filename.write_text(self.code, encoding="utf8")
        return filename

    def to_sys(self, module_name: str):
        import sys
        from types import ModuleType

        mod = ModuleType(module_name)
        sys.modules[module_name] = mod
        exec(self.code, mod.__dict__)

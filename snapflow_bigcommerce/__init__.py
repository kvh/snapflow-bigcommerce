from typing import TypeVar
from snapflow import SnapflowModule


ExampleSchema = TypeVar("ExampleSchema")

module = SnapflowModule(
    "example",
    py_module_path=__file__,
    py_module_name=__name__,
    schemas=["schemas/{example_schema}.yml"],
    snaps=[],
)
module.export()

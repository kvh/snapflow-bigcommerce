from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from snapflow import DataBlock, Function, FunctionContext, Param


@dataclass
class ExampleState:
    state_val: str


@Function(
    "example_function",
    namespace="{module name}",
    state_class=ExampleState,
)
@Param("example_api_key", "str")
def example_function(ctx: FunctionContext, block: DataBlock) -> pd.DataFrame[Any]:
    return block.as_dataframe()
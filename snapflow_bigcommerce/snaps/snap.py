from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from snapflow import DataBlock, Snap, SnapContext, Param


@dataclass
class ExampleState:
    state_val: str


@Snap(
    "example_snap",
    module="{module name}",
    state_class=ExampleState,
)
@Param("example_api_key", "str")
def example_snap(
    ctx: SnapContext, block: DataBlock
) -> pd.DataFrame[Any]:
    return block.as_dataframe()
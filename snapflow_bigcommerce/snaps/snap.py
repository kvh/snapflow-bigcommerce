from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from snapflow import DataBlock, Snap, SnapContext, Param


@dataclass
class BigcommerceState:
    state_val: str
    on_conflict: str


@Snap(
    "bigcommerce_snap",
    module="{bigcommerce}",
    state_class=BigcommerceState,
)
@Param("example_api_key", "str")
def example_snap(
    ctx: SnapContext, block: DataBlock
) -> pd.DataFrame[Any]:
    return block.as_dataframe()
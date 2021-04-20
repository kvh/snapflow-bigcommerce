BigCommerce module for the [snapflow](https://github.com/kvh/snapflow) framework.

#### Install

`pip install snapflow-bigcommerce` or `poetry add snapflow-bigcommerce`

#### Example

```python
from __future__ import annotations

from snapflow import Environment, graph_from_yaml, run
import snapflow_bigcommerce as bigcommerce

g = graph_from_yaml("""
nodes:
  - key: import_orders
    snap: bigcommerce.import_orders
    params:
      api_key: <API_KEY>
      store_id: <STORE_ID>
      from_date: 2020-01-01
      to_date: 2021-04-30
""")

env = Environment(
    modules=[bigcommerce, ],
)
run(g, env=env, node_timelimit_seconds=1)

# Get the final output block
with env.md_api.begin():
    datablock = env.get_latest_output("import_orders", g)
```

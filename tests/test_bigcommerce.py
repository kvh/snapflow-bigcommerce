import os
from dcp.utils.common import profile_stmt

import pytest

from snapflow import Environment
from snapflow.core.graph import graph


def ensure_api_key() -> str:
    api_key = os.environ.get("BIGCOMMERCE_API_KEY")
    if api_key is not None:
        return api_key
    api_key = input("Enter BigCommerce API key: ")
    return api_key


def ensure_store_id() -> str:
    sid = os.environ.get("BIGCOMMERCE_STORE_ID")
    if sid is not None:
        return sid
    sid = input("Enter BigCommerce store ID: ")
    return sid


def test_bigcommerce_orders():
    from snapflow_bigcommerce import module as snapflow_bigcommerce

    env = Environment(metadata_storage="sqlite://")
    env.add_module(snapflow_bigcommerce)

    g = graph()

    # Initial graph
    api_key = ensure_api_key()
    store_id = ensure_store_id()
    get_orders = g.create_node(
        snapflow_bigcommerce.functions.import_orders,
        params={"api_key": api_key, "store_id": store_id,},
    )

    blocks = env.produce(get_orders, g, execution_timelimit_seconds=2,)
    assert len(blocks[0].as_records()) > 0


def test_bigcommerce_order_products():
    from snapflow_bigcommerce import module as snapflow_bigcommerce

    env = Environment(metadata_storage="sqlite://")
    env.add_module(snapflow_bigcommerce)

    g = graph()

    # Initial graph
    api_key = ensure_api_key()
    store_id = ensure_store_id()
    get_orders = g.create_node(
        snapflow_bigcommerce.functions.import_order_products,
        params={"api_key": api_key, "store_id": store_id,},
    )

    blocks = env.produce(get_orders, g, execution_timelimit_seconds=2,)
    assert len(blocks[0].as_records()) > 0


if __name__ == "__main__":
    test_bigcommerce_orders()


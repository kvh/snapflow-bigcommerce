import pytest

from snapflow import Environment
from snapflow.core.graph import graph


@pytest.mark.parametrize("api_key")
@pytest.mark.parametrize("store_id")
def test_bigcommerce(api_key, store_id):
    run_test_bigcommerce(api_key, store_id)


def run_test_bigcommerce(api_key, store_id):
    from snapflow_bigcommerce import module as snapflow_bigcommerce

    env = Environment(metadata_storage="sqlite://")
    env.add_module(snapflow_bigcommerce)

    g = graph()

    # Initial graph
    get_orders = g.create_node(
        snapflow_bigcommerce.functions.import_orders,
        params={"api_key": api_key, "store_id": store_id,},
    )

    blocks = env.produce(get_orders, g, execution_timelimit_seconds=5,)
    assert len(blocks[0].as_records()) > 0


if __name__ == "__main__":
    api_key = input("Enter BigCommerce API key: ")
    store_id = input("Enter BigCommerce Store ID: ")

    test_bigcommerce(
        api_key=api_key, store_id=store_id,
    )


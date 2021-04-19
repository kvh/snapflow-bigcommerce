import pytest

from snapflow import Environment
from snapflow.core.graph import Graph
from snapflow.testing.utils import get_tmp_sqlite_db_url


@pytest.mark.parametrize("api_key")
@pytest.mark.parametrize("store_id")
def test_bigcommerce(api_key, store_id):
    run_test_bigcommerce(api_key, store_id)


def run_test_bigcommerce(api_key, store_id):
    import snapflow_bigcommerce

    env = Environment(metadata_storage="sqlite://")
    g = Graph(env)
    s = env.add_storage(get_tmp_sqlite_db_url())
    env.add_module(snapflow_bigcommerce)

    # Initial graph
    get_orders = g.create_node(
        'import_orders',
        params={
            "api_key": api_key,
            "store_id": store_id,
        },
    )

    output = env.produce(
        get_orders,
        g,
        target_storage=s,
        node_timelimit_seconds=0.01
    )
    records = output.as_records()
    assert len(records) > 0


if __name__ == "__main__":
    api_key = input("Enter BigCommerce API key: ")
    store_id = input("Enter BigCommerce Sore ID: ")

    test_bigcommerce(
        api_key=api_key,
        store_id=store_id,
    )

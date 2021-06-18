from snapflow import graph, produce


def test():
    import {module}

    g = graph()

    # Initial graph
    node1 = g.create_node(
        {module}.functions.{function name},
        params={"config_val": "val"},
    )
    blocks = produce(node1, modules=[{module}])
    records = blocks[0].as_records()
    assert len(records) > 0


if __name__ == "__main__":
    test()
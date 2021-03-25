from snapflow import graph, produce


def test():
    import {module}

    g = graph()

    # Initial graph
    node1 = g.create_node(
        {module}.snaps.{snap name},
        params={"config_val": "val"},
    )
    output = produce(node1, modules=[{module}])
    records = output.as_records()
    assert len(records) > 0


if __name__ == "__main__":
    test()
import cycles


def test_all_cycles_three_nodes_unlimited():
    node1 = '1'
    node2 = '2'
    node3 = '3'
    graph = {
        node1: {node2, node3},
        node2: {node1, node3},
        node3: {node2, node1}
    }
    result = cycles.get_all_cycles(
            graph=graph,
            start=node1
        )

    assert [node1, node2, node3, node1] in result
    assert [node1, node3, node2, node1] in result
    assert [node1, node3, node1] in result
    assert [node1, node2, node1] in result
    assert len(result) == 4


def test_all_cycles_three_nodes_one_way_block():
    node1 = '1'
    node2 = '2'
    node3 = '3'
    graph = {
        node1: {node2},
        node2: {node1, node3},
        node3: {node2, node1}
    }
    result = cycles.get_all_cycles(
            graph=graph,
            start=node1
        )

    assert [node1, node2, node3, node1] in result
    assert [node1, node2, node1] in result
    assert len(result) == 2


def test_all_full_cycles_two_nodes_unlimited():
    node1 = '1'
    node2 = '2'
    graph = {
        node1: {node2},
        node2: {node1}
    }
    result = cycles.get_all_full_cycles(
	graph=graph,
	start=node1
    )
    expected = [[node1, node2, node1]]
    assert result == expected


def test_all_full_cycles_three_nodes_unlimited():
    node1 = '1'
    node2 = '2'
    node3 = '3'
    graph = {
        node1: {node2, node3},
        node2: {node1, node3},
        node3: {node2, node1}
    }
    result = cycles.get_all_full_cycles(
        graph=graph,
        start=node1
    )
    assert [node1, node2, node3, node1] in result
    assert [node1, node3, node2, node1] in result
    assert len(result) == 2


def test_all_full_cycles_four_nodes_two_way_block():
    node1 = '1'
    node2 = '2'
    node3 = '3'
    node4 = '4'
    graph = {
        node1: {node2, node3},
        node2: {node1, node4},
        node3: {node1, node4},
        node4: {node2, node3}
    }
    result = cycles.get_all_full_cycles(
        graph=graph,
        start=node1
    )
    assert [node1, node2, node4, node3, node1] in result
    assert [node1, node3, node4, node2, node1] in result
    assert len(result) == 2


def test_all_full_cycles_four_nodes_one_way_block():
    node1 = '1'
    node2 = '2'
    node3 = '3'
    node4 = '4'
    graph = {
        node1: {node2, node3},
        node2: {node1, node3, node4},
        node3: {node1, node2, node4},
        node4: {node1, node2, node3}
    }
    result = cycles.get_all_full_cycles(
        graph=graph,
        start=node1
    )
    assert [node1, node2, node3, node4, node1] in result
    assert [node1, node2, node4, node3, node1] in result
    assert [node1, node3, node2, node4, node1] in result
    assert [node1, node3, node4, node2, node1] in result
    assert len(result) == 4



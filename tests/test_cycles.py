import cycles


def test_two_person_wichteling_unlimited():
    julian = 'Julian'
    paul = 'Paul'
    graph = {
        julian: {paul},
        paul: {julian}
    }
    result = cycles.get_all_cycles_of_length_n(
	graph=graph,
	start=julian,
	n_vertices=2
    )
    expected = [[julian, paul, julian]]
    assert result == expected


def test_three_person_wichteling_unlimited():
    julian = 'Julian'
    paul = 'Paul'
    ulrike = 'Ulrike'
    graph = {
        julian: {paul, ulrike},
        paul: {julian, ulrike},
        ulrike: {paul, julian}
    }
    result = cycles.get_all_cycles_of_length_n(
        graph=graph,
        start=julian,
	n_vertices=3
    )
    assert [julian, paul, ulrike, julian] in result
    assert [julian, ulrike, paul, julian] in result
    assert len(result) == 2


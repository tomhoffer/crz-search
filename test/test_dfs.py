import pytest as pytest

from indexer.model import Edge, EdgeType
from indexer.helpers import json_encode
from indexer.custom.indexer import EntityGraph


def vertex(v: str):
    return Edge(v, type=EdgeType.contract, contract=None)


def start_vertex(v: str):
    return Edge(v, type=EdgeType.start, contract=None)


class TestDfs:

    @pytest.fixture
    def default_graph(self):
        g = EntityGraph()
        default_graph = {
            'A': [vertex('B'), vertex('C'), vertex('F')],
            'B': [vertex('E'), vertex('A')],
            'C': [vertex('D'), vertex('E'), vertex('A')],
            'D': [vertex('F'), vertex('E'), vertex('C')],
            'E': [vertex('B'), vertex('C'), vertex('D')],
            'F': [vertex('D'), vertex('A')],
            'alone node': []
        }
        g.entity_graph = default_graph
        return g

    def test_find_all_paths(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'F')
        expected = [[start_vertex('A'), vertex('F')],
                    [start_vertex('A'), vertex('C'), vertex('D'), vertex('F')],
                    [start_vertex('A'), vertex('B'), vertex('E'), vertex('D'), vertex('F')],
                    [start_vertex('A'), vertex('C'), vertex('E'), vertex('D'), vertex('F')],
                    [start_vertex('A'), vertex('B'), vertex('E'), vertex('C'), vertex('D'), vertex('F')]]
        assert json_encode(results) == json_encode(expected)

    def test_path_to_itself(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'A')
        expected = [[start_vertex('A')]]
        assert json_encode(results) == json_encode(expected)

    def test_no_valid_path(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'alone node')
        expected = []
        assert json_encode(results) == json_encode(expected)

        results = default_graph.find_all_paths_iter('alone node', 'A')
        expected = []
        assert json_encode(results) == json_encode(expected)

    def test_only_within_range(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'D', range=3)
        expected = [[start_vertex('A'), vertex('C'), vertex('D')], [start_vertex('A'), vertex('F'), vertex('D')]]
        assert json_encode(results) == json_encode(expected)

        # Distance = 2, Range = 3
        results = default_graph.find_all_paths_iter('A', 'C', range=3)
        expected = [[start_vertex('A'), vertex('C')]]
        assert json_encode(results) == json_encode(expected)

        # Distance = 2, Range = 3
        results = default_graph.find_all_paths_iter('A', 'C', range=2)
        expected = [[start_vertex('A'), vertex('C')]]
        assert json_encode(results) == json_encode(expected)

        # Distance = 3, Range = 2
        results = default_graph.find_all_paths_iter('A', 'E', range=2)
        expected = []
        assert json_encode(results) == json_encode(expected)

    def test_multiple_vertices(self):
        g = EntityGraph()
        graph = {
            'A': [vertex('B'), vertex('B')],  # 2 vertices between A and B
            'B': [vertex('C'), vertex('A'), vertex('A')],
            'C': [vertex('B')],
        }

        g.entity_graph = graph

        results = g.find_all_paths_iter('A', 'C')
        expected = [[start_vertex('A'), vertex('B'), vertex('C')], [start_vertex('A'), vertex('B'), vertex('C')]]
        assert json_encode(results) == json_encode(expected)

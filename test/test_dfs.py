import pytest as pytest

from indexer.indexer import EntityGraph


class TestDfs:

    @pytest.fixture
    def default_graph(self):
        g = EntityGraph()
        default_graph = {
            'A': ['B', 'C', 'F'],
            'B': ['E', 'A'],
            'C': ['D', 'E', 'A'],
            'D': ['F', 'E', 'C', ],
            'E': ['B', 'C', 'D'],
            'F': ['D', 'A'],
            'alone node': []
        }
        g.entity_graph = default_graph
        return g

    def test_find_all_paths(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'F')
        expected = [['A', 'F'],
                    ['A', 'C', 'D', 'F'],
                    ['A', 'B', 'E', 'D', 'F'],
                    ['A', 'C', 'E', 'D', 'F'],
                    ['A', 'B', 'E', 'C', 'D', 'F']]
        assert results == expected

    def test_path_to_itself(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'A')
        expected = [['A']]
        assert results == expected

    def test_no_valid_path(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'alone node')
        expected = []
        assert results == expected

        results = default_graph.find_all_paths_iter('alone node', 'A')
        expected = []
        assert results == expected

    def test_only_within_range(self, default_graph):
        results = default_graph.find_all_paths_iter('A', 'D', range=3)
        expected = [['A', 'C', 'D'], ['A', 'F', 'D']]
        assert results == expected

        # Distance = 2, Range = 3
        results = default_graph.find_all_paths_iter('A', 'C', range=3)
        expected = [['A', 'C']]
        assert results == expected

        # Distance = 2, Range = 3
        results = default_graph.find_all_paths_iter('A', 'C', range=2)
        expected = [['A', 'C']]
        assert results == expected

        # Distance = 3, Range = 2
        results = default_graph.find_all_paths_iter('A', 'E', range=2)
        expected = []
        assert results == expected

    def test_multiple_vertices(self):
        g = EntityGraph()
        graph = {
            'A': ['B', 'B'],  # 2 vertices between A and B
            'B': ['C', 'A', 'A'],
            'C': ['B'],
        }
        g.entity_graph = graph

        results = g.find_all_paths_iter('A', 'C')
        expected = [['A', 'B', 'C'], ['A', 'B', 'C']]
        assert results == expected

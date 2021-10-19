import csv
from collections import deque
import numpy as np
from typing import List
from indexer.contract import Vertex, Contract

SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output.csv'


class EntityGraph:

    def __init__(self):
        self.entity_graph = {}

    def _add_to_graph(self, row):
        # Create contract relationship between customer and supplier
        contract = Contract(row)
        self._create_vertex(row['customer'], Vertex(target=row['supplier'], type='contract', contract=contract))
        self._create_vertex(row['supplier'], Vertex(target=row['customer'], type='contract', contract=contract))

        # Optional: Create relationship between customer and his address
        if row['customer_address']:
            self._create_vertex(row['customer'],
                                Vertex(target=row['customer_address'], type='address', contract=contract))
            self._create_vertex(row['customer_address'],
                                Vertex(target=row['customer'], type='address', contract=contract))

        # Optional: Create relationship between supplier and his address
        if row['supplier_address']:
            self._create_vertex(row['supplier'],
                                Vertex(target=row['supplier_address'], type='address', contract=contract))
            self._create_vertex(row['supplier_address'],
                                Vertex(target=row['supplier'], type='address', contract=contract))

    def _create_vertex(self, source_node: str, vertex: Vertex):
        try:
            self.entity_graph[source_node].append(vertex)
        except KeyError:
            self.entity_graph[source_node] = [vertex]

    def build_graph(self):
        print("Building the graph from the source file...")
        with open(SOURCE_FILE, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._add_to_graph(row)

    def find_all_paths_iter(self, src: str, dst: str, range: int = np.inf) -> List[List[Vertex]]:
        print("Finding paths in the graph...")
        all_paths_queue = deque()
        results: List[List[Vertex]] = []

        starting_vertex = Vertex(target=src, contract=None, type='start')
        current_path = [starting_vertex]
        all_paths_queue.append(current_path.copy())

        while all_paths_queue:
            current_path = all_paths_queue.popleft()
            current_vertex: Vertex = current_path[-1]

            current_path_len = len(current_path)
            if current_vertex.target == dst:
                results.append(current_path)

            for neighbor in self.entity_graph[current_vertex.target]:
                if current_path_len + 1 <= range and not any(d.target == neighbor.target for d in current_path):
                    newpath = [*current_path, neighbor]  # create shallow copy
                    all_paths_queue.append(newpath)
        return results

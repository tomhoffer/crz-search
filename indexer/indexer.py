import csv
from collections import deque
import numpy as np
from typing import List

SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output.csv'
MAX_PATH_LENGTH = 5


class EntityGraph:

    def __init__(self):
        self.entity_graph = {}

    def _add_to_graph(self, row):
        self._create_vertex(row['customer'], row['supplier'])
        self._create_vertex(row['supplier'], row['customer'])

    def _create_vertex(self, node_a: str, node_b: str):
        try:
            self.entity_graph[node_a].append(node_b)
        except KeyError:
            self.entity_graph[node_a] = [node_b]

    def build_graph(self):
        with open(SOURCE_FILE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._add_to_graph(row)

    def find_all_paths_iter(self, src: str, dst: str, range: int = np.inf) -> List[List[str]]:
        all_paths_queue = deque()
        results = []

        # Path vector to store the current path
        current_path = [src]
        all_paths_queue.append(current_path.copy())

        while all_paths_queue:
            current_path = all_paths_queue.popleft()
            current_node = current_path[-1]

            if current_node == dst:
                results.append(current_path)

            current_path_len = len(current_path)
            for neighbor in self.entity_graph[current_node]:
                if neighbor not in current_path and current_path_len + 1 <= range:
                    newpath = [*current_path, neighbor]  # create shallow copy
                    all_paths_queue.append(newpath)
        return results

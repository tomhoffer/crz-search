import csv
from collections import deque
import numpy as np
from typing import List, Dict

from helpers import pairwise

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
        print("Building the graph from the source file...")
        with open(SOURCE_FILE, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._add_to_graph(row)

    def find_all_paths_iter(self, src: str, dst: str, range: int = np.inf) -> List[List[str]]:
        print("Finding paths in the graph...")
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

    def find_all_paths_from_node(self, src: str, min_range = 0, max_range: int = np.inf) -> List[List[str]]:
        print("Finding paths in the graph...")
        all_paths_queue = deque()
        results = []

        # Path vector to store the current path
        current_path = [src]
        all_paths_queue.append(current_path.copy())

        while all_paths_queue:
            current_path = all_paths_queue.popleft()
            current_node = current_path[-1]

            current_path_len = len(current_path)

            if min_range < current_path_len <= max_range:
                results.append(current_path)

            for neighbor in self.entity_graph[current_node]:
                if neighbor not in current_path and current_path_len + 1 <= max_range:
                    newpath = [*current_path, neighbor]  # create shallow copy
                    all_paths_queue.append(newpath)
        return results

    # Find exact contract details for the path identified by self.find_all_paths_iter
    def find_contracts_for_given_paths(self, paths: List[List[str]]):
        pairs = []  # Pairs of contract parties of the given contract (customer, supplier)
        for path in paths:
            pairs.append([{'firstParty': el[0], 'secondParty': el[1], 'contract': None} for el in pairwise(path)])

        pairs = [p for sub in pairs for p in sub]  # Flatten
        print("Retrieving details of the identified contracts...")
        with open(SOURCE_FILE, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                unmatched = [pair for pair in pairs if not pair['contract']]
                for pair in unmatched:
                    if (row['customer'] == pair['firstParty'] and row['supplier'] == pair['secondParty']) or (
                            row['supplier'] == pair['firstParty'] and row['customer'] == pair['secondParty']):
                        pair['contract'] = row
        return pairs
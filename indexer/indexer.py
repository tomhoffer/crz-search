import csv
from collections import deque
import numpy as np
from typing import List
from parser.contract_parser import ContractParser
from indexer.model import Edge, Contract, Address, EdgeType

# SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output.csv'
SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output-mini.csv'


class EntityGraph:

    def __init__(self):
        self.entity_graph = {}
        self.cities = {}
        self.parser = ContractParser()

    def _add_address_to_graph(self, entity_name: str, address: Address, contract: Contract):
        if address.street:
            self._create_vertex(entity_name,
                                Edge(target=address.street, type=EdgeType.street, contract=contract))
            self._create_vertex(address.street,
                                Edge(target=entity_name, type=EdgeType.street, contract=contract))

            # Skip ZIP number
            # if address.zip:
            # self._create_vertex(entity_name,
            #                    Edge(target=address.zip, type=EdgeType.zip, contract=contract))
            # self._create_vertex(address.zip,
            #                    Edge(target=entity_name, type=EdgeType.zip, contract=contract))

        # if address.city:
        #    self._create_vertex(entity_name,
        #                        Edge(target=address.city, type=EdgeType.city, contract=contract))
        #    self._create_vertex(address.city,
        #                        Edge(target=entity_name, type=EdgeType.city, contract=contract))

    def _add_to_graph(self, row):
        # Create contract relationship between customer and supplier
        contract = Contract(row)
        self._create_vertex(row['customer'],
                            Edge(target=row['supplier'], type=EdgeType.contract, contract=contract))
        self._create_vertex(row['supplier'],
                            Edge(target=row['customer'], type=EdgeType.contract, contract=contract))

        # Optional: Create relationship between customer and his address
        if row['customer_address']:
            customer_address = self.parser.parse_address(row['customer_address'])
            self._add_address_to_graph(row['customer'], customer_address, contract)

        # Optional: Create relationship between supplier and his address
        if row['supplier_address']:
            supplier_address = self.parser.parse_address(row['supplier_address'])
            self._add_address_to_graph(row['supplier'], supplier_address, contract)

    def _create_vertex(self, source_node: str, vertex: Edge):
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

    def find_all_paths_iter(self, src: str, dst: str, range: int = np.inf) -> List[List[Edge]]:
        print("Finding paths in the graph...")
        all_paths_queue = deque()
        results: List[List[Edge]] = []

        starting_vertex = Edge(target=src, contract=None, type=EdgeType.start)
        current_path = [starting_vertex]
        all_paths_queue.append(current_path.copy())

        while all_paths_queue:
            current_path = all_paths_queue.popleft()
            current_vertex: Edge = current_path[-1]

            current_path_len = len(current_path)
            if current_vertex.target == dst:
                results.append(current_path)

            for neighbor in self.entity_graph[current_vertex.target]:
                if current_path_len + 1 <= range and not any(d.target == neighbor.target for d in current_path):
                    newpath = [*current_path, neighbor]  # create shallow copy
                    all_paths_queue.append(newpath)
        self._print_paths(results)
        return results

    def _print_paths(self, paths: List[List[Edge]]):
        print('Found paths:')
        for path in paths:
            for i in range(len(path)):
                print("({}, {})".format(path[i].type.value, path[i].target), end="")
                if i != len(path) - 1:
                    print(" -> ", end="")
            print("")

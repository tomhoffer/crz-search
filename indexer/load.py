import csv
from queue import Queue

SOURCE_FILE = '../output.csv'


def add_to_graph(entity_graph, row):
    create_vertex(entity_graph, row['customer'], row['supplier'])
    create_vertex(entity_graph, row['supplier'], row['customer'])


def create_vertex(entity_graph, node_a: str, node_b: str):
    try:
        entity_graph[node_a].append(node_b)
    except KeyError:
        entity_graph[node_a] = [node_b]

# TODO pridat do hran atributy zmluvy
def build_graph():
    entity_graph = {}
    with open(SOURCE_FILE) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            add_to_graph(entity_graph, row)
    return entity_graph


def bfs(visited_nodes, queue: Queue, entity_graph, node):
    visited_nodes.append(node)
    queue.put(node)

    while not queue.empty():
        s = queue.get()
        for neighbour in entity_graph[s]:
            if neighbour not in visited_nodes:
                visited_nodes.append(neighbour)
                queue.put(neighbour)


visited = []
queue = Queue()
entity_graph = build_graph()

bfs(visited, queue, entity_graph, 'HOTEL TURIEC, a.s.')

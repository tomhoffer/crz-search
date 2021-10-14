from indexer import EntityGraph

entity_graph = EntityGraph()
entity_graph.build_graph()
# entity_graph.find_all_paths_recursive('HOTEL TURIEC, a.s.', 'RENT2B, s.r.o.')
result = entity_graph.find_all_paths_iter('Nadácia ESET	', 'ALFA LAVAL Slovakia s.r.o.', range=8)
print(result)
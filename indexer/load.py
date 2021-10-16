import json

from indexer import EntityGraph

entity_graph = EntityGraph()
entity_graph.build_graph()
results = entity_graph.find_all_paths_iter('DOXX – Stravné lístky spol. s r. o.', 'BRATIA SABOVCI, s.r.o.', range=5)
#results = entity_graph.find_all_paths_from_node('DOXX – Stravné lístky spol. s r. o.', min_range=3, max_range=5)
print("Found paths:")
print(results)

print("Details of the contracts:")
details = entity_graph.find_contracts_for_given_paths(results)
print(json.dumps(details, indent=4, ensure_ascii=False))

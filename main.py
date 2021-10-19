from indexer.helpers import json_encode

from indexer.EntityGraph

entity_graph = EntityGraph()
entity_graph.build_graph()
#results = entity_graph.find_all_paths_iter('DOXX – Stravné lístky spol. s r. o.', 'BRATIA SABOVCI, s.r.o.', range=3)
results = entity_graph.find_all_paths_iter('Všeobecná zdravotná poisťovňa, a.s.', 'Slovenská pošta, a. s.', range=3)
# results = entity_graph.find_all_paths_from_node('Všeobecná zdravotná poisťovňa, a.s.', min_range=3, max_range=5)
print("Found paths:")
print(json_encode(results))

# print("Details of the contracts:")
# details = entity_graph.find_contracts_for_given_paths(results)
# print(json.dumps(details, indent=4, ensure_ascii=False))

from indexer.helpers import json_encode
from indexer.indexer import EntityGraph

entity_graph = EntityGraph()
entity_graph.build_graph()
#results = entity_graph.find_all_paths_iter('DOXX – STRAVNÉ LÍSTKY SPOL. S R. O.', 'BRATIA SABOVCI, S.R.O.', range=3)
results = entity_graph.find_all_paths_iter('Zvolen', 'BRATIA SABOVCI, S.R.O.', range=4)
#results = entity_graph.find_all_paths_iter('Všeobecná zdravotná poisťovňa, a.s.', 'Slovenská pošta, a. s.', range=3)
#results = entity_graph.find_all_paths_from_node('Záhradnícka 151, Bratislava 821 08', min_range=1, max_range=5)
print("Found paths:")
print(json_encode(results))

# print("Details of the contracts:")
# details = entity_graph.find_contracts_for_given_paths(results)
# print(json.dumps(details, indent=4, ensure_ascii=False))

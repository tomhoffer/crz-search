from indexer.indexer import EntityGraph

entity_graph = EntityGraph()
entity_graph.build_graph()

# Example: Same city
# results = entity_graph.find_all_paths_iter('V. D. S. SPOL. S R. O.', 'ENBRA SLOVAKIA S.R.O.', range=3)

# Example: Enclosed contract
# results = entity_graph.find_all_paths_iter('DOXX – STRAVNÉ LÍSTKY SPOL. S R. O.', 'BRATIA SABOVCI, S.R.O.', range=3)

# Example: Same address
#results = entity_graph.find_all_paths_iter('SLOVAK TELEKOM, A. S.', 'T MOBILE SLOVAK TELEKOM, A.S.', range=3)



results = entity_graph.find_all_paths_iter('SLOVENSKÁ POĽNOHOSPODÁRSKA UNIVERZITA V NITRE', 'T MOBILE SLOVAK TELEKOM, A.S.', range=4)



# print(json_encode(results))

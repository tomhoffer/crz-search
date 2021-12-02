import csv
from dataclasses import dataclass
from typing import Optional, Dict
from indexer.model import EdgeType, Contract, Address
from parser.contract_parser import ContractParser

#SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output-mini.csv'
SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output.csv'
OUTPUT_VERTICES = '/Users/tomashoffer/Documents/Coding-Projects/vinf/vertices.csv'
OUTPUT_EDGES = '/Users/tomashoffer/Documents/Coding-Projects/vinf/edges.csv'


@dataclass
class Vertex:
    id: str

    def __init__(self, id: str):
        self.id = id


@dataclass
class Edge:
    src: str
    dst: str
    type: EdgeType
    contract: Optional[Contract]

    def __init__(self, src: str, dst: str, type: EdgeType, contract: Optional[Contract]):
        self.src = src
        self.dst = dst
        self.type = type
        self.contract = contract


def write_edge(e: Edge, writer):
    writer.writerow(
        [e.src, e.dst, e.type, e.contract.url, e.contract.id, e.contract.number, e.contract.resort,
         e.contract.customer,
         e.contract.customer_address, e.contract.supplier, e.contract.supplier_address, e.contract.name,
         e.contract.note, e.contract.final_price_eur, e.contract.publication_date, e.contract.conclusion_date,
         e.contract.effective_date, e.contract.expiration_date])


def write_address(address: str, entity: Vertex, contract: Contract, parser: ContractParser, vertex_writer, edge_writer):
    entity_address: Address = parser.parse_address(address)
    city_vertex = Vertex(id=entity_address.city)
    street_vertex = Vertex(id=entity_address.street)
    zip_vertex = Vertex(id=entity_address.zip)

    if city_vertex.id:
        e_entity_city = Edge(src=entity.id, dst=city_vertex.id, type=EdgeType.city.value, contract=contract)
        e_city_entity = Edge(src=city_vertex.id, dst=entity.id, type=EdgeType.city.value, contract=contract)
        write_edge(e_entity_city, edge_writer)
        write_edge(e_city_entity, edge_writer)
        vertex_writer.writerow([city_vertex.id])

    if street_vertex.id:
        e_entity_street = Edge(src=entity.id, dst=street_vertex.id, type=EdgeType.street.value, contract=contract)
        e_street_entity = Edge(src=street_vertex.id, dst=entity.id, type=EdgeType.street.value, contract=contract)
        write_edge(e_entity_street, edge_writer)
        write_edge(e_street_entity, edge_writer)
        vertex_writer.writerow([street_vertex.id])

    #if zip_vertex.id:
    #    e_entity_zip = Edge(src=entity.id, dst=zip_vertex.id, type=EdgeType.zip.value, contract=contract)
    #    e_zip_entity = Edge(src=zip_vertex.id, dst=entity.id, type=EdgeType.zip.value, contract=contract)
    #    write_edge(e_entity_zip, edge_writer)
    #    write_edge(e_zip_entity, edge_writer)
    #    vertex_writer.writerow([zip_vertex.id])


def add_to_graph(row: Dict, parser: ContractParser):
    with open(OUTPUT_VERTICES, 'a') as f1, open(OUTPUT_EDGES, 'a') as f2:
        vertex_writer = csv.writer(f1)
        edge_writer = csv.writer(f2)

        # Create contract relationship between customer and supplier
        contract = Contract(row)
        customer = Vertex(id=row['customer'])
        supplier = Vertex(id=row['supplier'])
        e1 = Edge(src=customer.id, dst=supplier.id, type=EdgeType.contract.value, contract=contract)
        e2 = Edge(src=supplier.id, dst=customer.id, type=EdgeType.contract.value, contract=contract)

        write_edge(e1, edge_writer)
        write_edge(e2, edge_writer)
        vertex_writer.writerow([customer.id])
        vertex_writer.writerow([supplier.id])

        # Optional: Create relationship between customer and his address
        if row['customer_address']:
            write_address(address=row['customer_address'], entity=customer, contract=contract, parser=parser,
                          vertex_writer=vertex_writer, edge_writer=edge_writer)

        # Optional: Create relationship between supplier and his address
        if row['supplier_address']:
            write_address(address=row['supplier_address'], entity=supplier, contract=contract, parser=parser,
                          vertex_writer=vertex_writer, edge_writer=edge_writer)


with open(SOURCE_FILE, encoding="utf8") as csvfile:
    # Write csv headers
    with open(OUTPUT_VERTICES, 'w') as f:
        writer = csv.writer(f)
        header = ['id']
        writer.writerow(header)
    with open(OUTPUT_EDGES, 'w') as f:
        writer = csv.writer(f)
        header = ['src', 'dst', 'type', 'url', 'id', 'number', 'resort', 'customer', 'customer_address', 'supplier',
                  'supplier_address', 'name', 'note', 'final_price_eur', 'publication_date', 'conclusion_date',
                  'effective_date', 'expiration_date']
        writer.writerow(header)

    reader = csv.DictReader(csvfile)
    parser = ContractParser()
    for row in reader:
        add_to_graph(row, parser)

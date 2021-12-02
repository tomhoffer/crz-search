import csv
from typing import Dict
from indexer.model import Address
from parser.contract_parser import ContractParser

base_path = '/Users/tomashoffer/Documents/Coding-Projects/vinf/indexer/neo4j_data/'
SOURCE_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/output.csv'

OUTPUT_COMPANIES = base_path + 'companies.csv'
OUTPUT_STREETS = base_path + 'streets.csv'
OUTPUT_CITIES = base_path + 'cities.csv'
OUTPUT_ZIPS = base_path + 'zips.csv'
OUTPUT_CONTRACT_RELATIONSHIPS = base_path + 'relationships_contract.csv'
OUTPUT_STREET_RELATIONSHIPS = base_path + 'relationships_street.csv'
OUTPUT_CITY_RELATIONSHIPS = base_path + 'relationships_city.csv'
OUTPUT_ZIP_RELATIONSHIPS = base_path + 'relationships_zip.csv'

unique_companies = {}
unique_cities = {}
unique_city_relationships = {}
unique_streets = {}
unique_street_relationships = {}
unique_zips = {}
unique_zip_relationships = {}


def write_address(address: Address, entity: str, city_writer, zip_writer, street_writer,
                  city_relationship_writer, zip_relationship_writer, street_relationship_writer):
    if address.city:
        if address.city not in unique_cities:
            city_writer.writerow([address.city, 'City'])
            unique_cities[address.city] = True
        if entity + address.city not in unique_city_relationships:
            city_relationship_writer.writerow([entity, address.city, 'resides'])
            unique_city_relationships[entity + address.city] = True

    if address.zip:
        if address.zip not in unique_zips:
            zip_writer.writerow([address.zip, 'Zip'])
            unique_zips[address.zip] = True
        if entity + address.zip not in unique_zip_relationships:
            zip_relationship_writer.writerow([entity, address.zip, 'resides'])
            unique_zip_relationships[entity + address.zip] = True

    if address.street:
        if address.street not in unique_streets:
            street_writer.writerow([address.street, 'Street'])
            unique_streets[address.street] = True
        if entity + address.street not in unique_street_relationships:
            street_relationship_writer.writerow([entity, address.street, 'resides'])
            unique_street_relationships[entity + address.street] = True


def process_item(row: Dict, company_writer, city_writer, street_writer, zip_writer,
                 contract_relationship_writer, zip_relationship_writer, city_relationship_writer,
                 street_relationship_writer, parser: ContractParser):
    # Create company entity for customer and supplier
    if not row['customer'] in unique_companies:
        company_writer.writerow([row['customer'], 'Company'])
        unique_companies[row['customer']] = True

    if not row['supplier'] in unique_companies:
        company_writer.writerow([row['supplier'], 'Company'])
        unique_companies[row['supplier']] = True

    # Create contract relationship between customer and supplier
    contract_relationship_writer.writerow(
        [row['customer'], row['supplier'], 'contract', row['url'], row['id'], row['type'], row['number'], row['resort'],
         row['name'], row['note'], row['final_price_eur'], row['publication_date'], row['conclusion_date'],
         row['effective_date'], row['expiration_date']])

    # Optional: Create relationship between customer and his address
    if row['customer_address']:
        customer_address: Address = parser.parse_address(row['customer_address'])
        write_address(customer_address, row['customer'], city_writer, zip_writer, street_writer,
                      city_relationship_writer, zip_relationship_writer, street_relationship_writer)

    # Optional: Create relationship between supplier and his address
    if row['supplier_address']:
        supplier_address: Address = parser.parse_address(row['supplier_address'])
        write_address(supplier_address, row['supplier'], city_writer, zip_writer, street_writer,
                      city_relationship_writer, zip_relationship_writer, street_relationship_writer)


with open(SOURCE_FILE, encoding="utf8") as csvfile, \
        open(OUTPUT_COMPANIES, 'w') as companies, \
        open(OUTPUT_STREETS, 'w') as streets, \
        open(OUTPUT_CITIES, 'w') as cities, \
        open(OUTPUT_ZIPS, 'w') as zips, \
        open(OUTPUT_CITY_RELATIONSHIPS, 'w') as city_relationships, \
        open(OUTPUT_STREET_RELATIONSHIPS, 'w') as street_relationships, \
        open(OUTPUT_ZIP_RELATIONSHIPS, 'w') as zip_relationships, \
        open(OUTPUT_CONTRACT_RELATIONSHIPS, 'w') as contract_relationships:
    reader = csv.DictReader(csvfile)
    parser = ContractParser()

    company_writer = csv.writer(companies)
    city_writer = csv.writer(cities)
    street_writer = csv.writer(streets)
    zip_writer = csv.writer(zips)
    contract_relationship_writer = csv.writer(contract_relationships)
    zip_relationship_writer = csv.writer(zip_relationships)
    city_relationship_writer = csv.writer(city_relationships)
    street_relationship_writer = csv.writer(street_relationships)

    for row in reader:
        process_item(row, company_writer, city_writer, street_writer, zip_writer,
                     contract_relationship_writer, zip_relationship_writer, city_relationship_writer,
                     street_relationship_writer, parser)

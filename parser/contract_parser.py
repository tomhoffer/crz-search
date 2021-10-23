import csv
import re
from typing import Optional, Tuple, List

from indexer.model import Address

# Source: https://www.geoportal.sk/sk/zbgis_smd/na-stiahnutie/
CITIES_FILE = '/Users/tomashoffer/Documents/Coding-Projects/vinf/slovakia_cities.csv'


class ContractParser:
    cities = {}

    def __init__(self):
        print("Building the list of cities and villages in Slovakia...")
        with open(CITIES_FILE, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                self.cities[row['NM3']] = True  # City
                self.cities[row['NM4']] = True  # Village

                # Special cases, such as Bratislava-Nové Mesto
                city_dashed = row['NM4'].split('-')
                if len(city_dashed) > 1:
                    self.cities[city_dashed[0]] = True

        print("Indexed ", len(self.cities), " cities and villages.")

    def parse_date(self, text: str) -> Optional[str]:
        try:
            text = text.replace('-', '.').replace('/', '.')
            res = re.search(r'\d\d?\.\d*\d?\.\d\d\d\d', text).group(0)
            return res
        except AttributeError:  # Regex not matched
            return None

    def parse_contract_party(self, text: List[str]) -> Tuple[Optional[str], Optional[str]]:
        if not any(text):
            return None, None
        name = text[0]
        try:
            address = text[1] if text[1] else None
            return name, address
        except IndexError:
            return name, None

    def parse_price(self, text: str) -> Optional[float]:
        try:
            res = re.search(r'\d*\s?\d*[.,]?\d*', text).group(0).replace(',', '.').replace(' ', '')
            return float(res)
        except (AttributeError, ValueError):  # Regex not matched
            return None

    def parse_address(self, text: str) -> Address:
        zip_code = None
        city = None
        street = None

        if not text:
            return Address(zip=None, city=None, street=None)

        # Reduce multiple spaces to 1
        text = re.sub(' +', ' ', text)

        # Zip code
        try:
            zip_match = re.search(r'\d\d\d ?\d\d', text)
            zip_code = zip_match.group(0)
            text = text.replace(zip_code, '')
            zip_code = zip_code.replace(' ', '')
        except AttributeError:  # Regex not matched
            pass

        # City
        matches = re.findall(r'[a-žA-Ž]+ ?[a-žA-Ž]* ?[a-žA-Ž]*', text)
        for match in matches:
            try:
                match = match.strip()
                if self.cities[match]:
                    city = match
                    break
            except KeyError:
                continue

        if city:
            text = text.replace(city, '')

        # Street
        try:
            street = re.search(r'[a-žA-Ž]+(( \d+\/?\d*)|( č. \d+\/?\d*)|( ulica č. \d+\/?\d*))', text).group(0)
        except AttributeError:
            pass

        return Address(zip=zip_code, city=city, street=street)

    def parse_string(self, text: str) -> Optional[str]:
        return text if text else None

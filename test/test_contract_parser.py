import pytest as pytest

from indexer.model import Address
from parser.contract_parser import ContractParser


class TestContractParser:

    @pytest.fixture
    def parser(self):
        return ContractParser()

    def test_parse_date(self, parser):
        # Input: Expected output
        test_data = {
            '02.10.2021': '02.10.2021',
            '2.10.2021': '2.10.2021',
            '2.8.2021': '2.8.2021',
            'neznámy': None,
            '': None,
            '2.8': None,
            '2.8.202': None,

            '02-10-2021': '02.10.2021',
            '2-10-2021': '2.10.2021',
            '2-8-2021': '2.8.2021',

            '02/10/2021': '02.10.2021',
            '2/10/2021': '2.10.2021',
            '2/8/2021': '2.8.2021',
        }

        for key, value in test_data.items():
            assert parser.parse_date(key) == value

    def test_parse_price(self, parser):
        # Input: Expected output
        test_data = {
            '170,0 EUR': 170.0,
            '170.0 EUR': 170.0,
            '170,00 €': 170.0,
            '170.0': 170.0,
            '170,0': 170.0,
            '170': 170.0,
            '7 178,17 €': 7178.17,
            '389 240,71 €': 389240.71,
            '389 240,0 €': 389240.0,
            '389 240 €': 389240.0,
            'neznámy': None,
            '': None,
        }

        for key, value in test_data.items():
            assert parser.parse_price(key) == value

    def test_parse_contract_party(self, parser):

        assert parser.parse_contract_party(
            ['Úrad pre verejné obstarávanie', 'Ružová dolina 10, 821 09 Bratislava']) == (
                   'Úrad pre verejné obstarávanie', 'Ružová dolina 10, 821 09 Bratislava')

        assert parser.parse_contract_party(['Úrad pre verejné obstarávanie']) == (
            'Úrad pre verejné obstarávanie', None)

        assert parser.parse_contract_party(['Úrad pre verejné obstarávanie', '']) == (
            'Úrad pre verejné obstarávanie', None)

    def test_parse_string(self, parser):

        # Input: Expected output
        test_data = {
            'test': 'test',
            '': None,
            None: None
        }

        for key, value in test_data.items():
            assert parser.parse_string(key) == value

    def test_parse_address(self, parser):

        # Input: Expected output
        test_data = {

            # Street names in different forms
            'Štefanovičova 4, 816 23 Bratislava 1': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Štefanovičova 48, 816 23 Bratislava 1': Address(zip='81623', city='Bratislava', street='Štefanovičova 48'),
            'Štefanovičova č. 48, 816 23 Bratislava 1': Address(zip='81623', city='Bratislava', street='Štefanovičova č. 48'),
            'Štefanovičova ulica č. 48, 816 23 Bratislava 1': Address(zip='81623', city='Bratislava', street='Štefanovičova ulica č. 48'),
            'Ul. Štefanovičova 4 , P. O. Box 76  , 810 05 Bratislava 1': Address(zip='81005', city='Bratislava', street='Štefanovičova 4'),
            'Štefánikova 3707/57, 058 01 Poprad': Address(zip='05801', city='Poprad', street='Štefánikova 3707/57'),
            'Štefánikova ulica č. 3707/57, 058 01 Poprad': Address(zip='05801', city='Poprad', street='Štefánikova ulica č. 3707/57'),
            'Ul. Víťazná č. 802/18, 958 01 Partizánske': Address(zip='95801', city='Partizánske', street='Víťazná č. 802/18'),
            'Štefanovičova 4 , P. O. Box 76  , 810 05 Bratislava 1': Address(zip='81005', city='Bratislava', street='Štefanovičova 4'),

            # Street missing
            'Štrkovec 134': Address(zip=None, city='Štrkovec', street=None),

            # Address with and without commas
            'Štefanovičova 4, 816 23 Bratislava': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Štefanovičova 4, 816 23, Bratislava': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Štefanovičova 4 816 23 Bratislava': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),

            # City names
            'Štefanovičova 4, 816 23, Bratislava 2': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Štefanovičova 4, 816 23, Bratislava-Nové Mesto': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Vajanského 33, 052 01 Spišská Nová Ves': Address(zip='05201', city='Spišská Nová Ves', street='Vajanského 33'),
            'Bratislava': Address(city='Bratislava'),
            'Štôla': Address(city='Štôla'),
            'Spišská Nová Ves': Address(zip=None, city='Spišská Nová Ves', street=None),

            # Various order
            'Bratislava, Štefanovičova 4, 816 23': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            'Bratislava, 816 23, Štefanovičova 4': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),
            '816 23, Bratislava, Štefanovičova 4': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),

            # Zip code with and without space
            'Bratislava, 81623, Štefanovičova 4': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),

            # Country name included
            'Štefanovičova 4, 816 23, Bratislava, Slovenská republika': Address(zip='81623', city='Bratislava', street='Štefanovičova 4'),

            # Empty
            '': Address(zip=None, city=None, street=None),
            None: Address(zip=None, city=None, street=None),
        }

        for key, value in test_data.items():
            assert parser.parse_address(key) == value

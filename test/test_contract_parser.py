from crawler.contract_parser import parse_date, parse_price, parse_contract_party, parse_string


class TestContractParser:

    def test_parse_date(self):
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
            assert parse_date(key) == value

    def test_parse_price(self):
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
            assert parse_price(key) == value

    def test_parse_contract_party(self):

        assert parse_contract_party(['Úrad pre verejné obstarávanie', 'Ružová dolina 10, 821 09 Bratislava']) == (
            'Úrad pre verejné obstarávanie', 'Ružová dolina 10, 821 09 Bratislava')

        assert parse_contract_party(['Úrad pre verejné obstarávanie']) == (
            'Úrad pre verejné obstarávanie', None)

        assert parse_contract_party(['Úrad pre verejné obstarávanie', '']) == (
            'Úrad pre verejné obstarávanie', None)

    def test_parse_string(self):

        # Input: Expected output
        test_data = {
            'test': 'test',
            '': None,
            None: None
        }

        for key, value in test_data.items():
            assert parse_string(key) == value

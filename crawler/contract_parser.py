import re
from typing import Optional, Tuple, List


def parse_date(text: str) -> Optional[str]:
    try:
        text = text.replace('-', '.').replace('/', '.')
        res = re.search(r'\d\d?\.\d*\d?\.\d\d\d\d', text).group(0)
        return res
    except AttributeError:  # Regex not matched
        return None


def parse_contract_party(text: List[str]) -> Tuple[Optional[str], Optional[str]]:
    if not any(text):
        return None, None
    name = text[0]
    try:
        address = text[1] if text[1] else None
        return name, address
    except IndexError:
        return name, None


def parse_price(text: str) -> Optional[float]:
    try:
        res = re.search(r'\d*[.,]?\d*', text).group(0).replace(',', '.')
        return float(res)
    except (AttributeError, ValueError):  # Regex not matched
        return None


def parse_string(text: str) -> Optional[str]:
    return text if text else None

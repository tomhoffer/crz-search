import sys
from typing import Literal, Optional


class Contract:
    url: str
    id: str
    type: str
    number: str
    resort: str
    customer: str
    customer_address: str
    supplier: str
    supplier_address: str
    name: str
    note: str
    final_price_eur: float
    publication_date: str
    conclusion_date: str
    effective_date: str
    expiration_date: str

    def __init__(self, obj):
        self.url = obj['url']
        self.id = obj['id']
        self.type = obj['type']
        self.number = obj['number']
        self.resort = obj['resort']
        self.customer = obj['customer']
        self.customer_address = obj['customer_address']
        self.supplier = obj['supplier']
        self.supplier_address = obj['supplier_address']
        self.name = obj['name']
        self.note = obj['note']
        self.final_price_eur = float(obj['final_price_eur']) if obj['final_price_eur'] else None
        self.publication_date = obj['publication_date']
        self.conclusion_date = obj['conclusion_date']
        self.effective_date = obj['effective_date']
        self.expiration_date = obj['expiration_date']


class Vertex:
    target: str  # E.g. supplier name, address value,...
    type: Literal['address', 'contract', 'start']
    contract: Optional[Contract]

    def __init__(self, target: str, type: Literal['address', 'contract', 'start'], contract: Optional[Contract]):
        self.target = target
        self.type = type
        self.contract = contract

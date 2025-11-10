from dataclasses import dataclass

@dataclass
class Retailer:
    """
    Nodo del grafo: rappresenta un rivenditore.
    Attributi:
        retailer_id: identificativo univoco
        retailer_name: nome del rivenditore
        country: nazione
    """
    retailer_id: int
    retailer_name: str
    country: str

    def __hash__(self):
        # Serve per poter usare il Retailer come nodo di un grafo NetworkX
        return hash(self.retailer_id)

    def __eq__(self, other):
        if isinstance(other, Retailer):
            return self.retailer_id == other.retailer_id
        return False

    def __str__(self):
        return f"{self.retailer_name} ({self.country})"

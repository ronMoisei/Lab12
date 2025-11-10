from dataclasses import dataclass

@dataclass
class Arco:
    """
    Rappresenta un arco non orientato tra due retailer.
    Attributi:
        v1: primo nodo (Retailer)
        v2: secondo nodo (Retailer)
        peso: peso dell’arco (numero di prodotti in comune)
    """
    v1: object
    v2: object
    peso: int

    def __str__(self):
        return f"{self.v1.retailer_name} — {self.v2.retailer_name}  (peso={self.peso})"

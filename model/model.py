import networkx as nx
from database.DAO import DAO
from model.Arco import Arco
from model.retailer import Retailer


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    # -------------------------------------------------
    # 1) COSTRUZIONE GRAFO
    # -------------------------------------------------
    def buildGraph(self, country: str, year: int):
        """
        Costruisce il grafo:
        - nodi: retailer della nazione indicata
        - archi: collegano due retailer se hanno venduto almeno
          un prodotto in comune nello stesso anno.
        """
        # Pulisce il grafo precedente
        self._graph.clear()

        # 1. Ottieni i retailer per nazione
        retailers = DAO.getAllRetailersByCountry(country)
        self._idMap = {r.retailer_id: r for r in retailers}
        self._graph.add_nodes_from(retailers)

        # 2. Ottieni gli archi (peso = num prodotti in comune)
        edges = DAO.getAllEdges(country, year, self._idMap)
        for arco in edges:
            self._graph.add_edge(arco.v1, arco.v2, weight=arco.peso)

        return self.getGraphDetails()

    # -------------------------------------------------
    # 2) INFORMAZIONI SUL GRAFO
    # -------------------------------------------------
    def getGraphDetails(self):
        n_nodes = self._graph.number_of_nodes()
        n_edges = self._graph.number_of_edges()
        return n_nodes, n_edges

    def getAllNodes(self):
        return list(self._graph.nodes)

    # -------------------------------------------------
    # 3) VOLUME DI OGNI RETAILER
    # -------------------------------------------------
    def getRetailersVolume(self):
        """
        Restituisce una lista di tuple (Retailer, volume)
        dove volume = somma dei pesi degli archi incidenti al nodo.
        """
        volumes = []
        for node in self._graph.nodes:
            volume = sum(data["weight"] for _, _, data in self._graph.edges(node, data=True))
            volumes.append((node, volume))

        # ordina per volume decrescente
        volumes.sort(key=lambda x: x[1], reverse=True)
        return volumes

    # -------------------------------------------------
    # 4) UTILITÀ
    # -------------------------------------------------
    def printGraphDetails(self):
        n_nodes, n_edges = self.getGraphDetails()
        print(f"Grafo creato con {n_nodes} nodi e {n_edges} archi.")

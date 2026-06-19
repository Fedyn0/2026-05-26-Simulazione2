import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self._idMapNames = {}
        for name in DAO.getAllNames():
            self._idMapNames[name.id] = name

    def getAllRatings(self):
        return DAO.getAllRatings()

    def creaGrafo(self, voto1, voto2):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(voto1, voto2)
        self._grafo.add_nodes_from(self._nodes)

        for node in self._nodes:
            self._idMapNames[node.id] = node

        for u, v, peso in DAO.getAllEdges(voto1, voto2):
            actor1 = self._idMapNames[u]
            actor2 = self._idMapNames[v]

            if actor1 in self._nodes and actor2 in self._nodes:
                self._grafo.add_edge(actor1, actor2, weight=peso)


    def getCompConn(self):
        compconn = list(nx.connected_components(self._grafo))
        largest = max(compconn, key=len)

        return len(compconn), largest

    def getDettagliGrafo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getArchiPesoMaggiore(self):

        archi = list(self._grafo.edges(data=True))
        archi.sort(key = lambda x:x[2]["weight"], reverse = True)
        nuovaLista = []
        for i in archi:
            nuovaLista.append((i[0], i[1], i[2]["weight"]))


        return nuovaLista[0:5]



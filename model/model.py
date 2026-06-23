import copy
from database.dao import Dao
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._users_list = []
        self.load_all_users()
        self.G = nx.Graph()
        self.users_map = {}
        self.best_path = []
        self.best_score = 0


    def load_all_users(self):
        self._users_list = Dao.read_all_users()
        self.users_map = {u.user_id: u for u in self._users_list}
        print(f"Users: {self._users_list}")


    def build_graph(self, n_bus):
        self.G.clear()
        counts = Dao.get_business_counts()
        for u in self._users_list:
            if counts.get(u.user_id, 0) >= n_bus:
                self.G.add_node(u.user_id, artist = u)
        coppie = Dao.get_shared_businesses()
        for u1, u2, peso in coppie:
            if u1 in self.G.nodes() and u2 in self.G.nodes():
                self.G.add_edge(u1, u2, weight = peso)

        return self.G

    def num_nodi(self):
        return self.G.number_of_nodes()
    def num_archi(self):
        return self.G.number_of_edges()
    def get_nodi_grafo(self):
        return [data['artist']for _,data in self.G.nodes(data=True)]


    def classifica(self):
        result = []
        for node in self.G.nodes():
            strenght = sum(e['weight'] for _,_,e in self.G.edges(node, data=True))
            result.append((self.G.nodes[node]['artist'], strenght))

        return sorted(result, key = lambda x: x[1], reverse = True)

    def get_best_path(self, lunghezza, start_id):
        self.best_path = []
        self.best_score = 0
        self._ricorsione([start_id], lunghezza)
        return self.best_path, self.best_score

    def _ricorsione(self, parziale, lunghezza):
        if len(parziale) == lunghezza:
            score = self._get_score(parziale)
            if score > self.best_score:
                self.best_path = copy.deepcopy(parziale)
                self.best_score = score
            return

        ultimo = parziale[-1]
        for succ in self.G.neighbors(ultimo):
            if succ not in parziale:
                parziale.append(succ)
                self._ricorsione(parziale, lunghezza)
                parziale.pop()

    def _get_score(self, percorso):
        score = 0
        for i in range(1, len(percorso)):
            score += self.G[percorso[i-1]][percorso[i]]['weight']
        return score
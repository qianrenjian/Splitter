import random
import numpy as np
from tqdm import tqdm
import networkx as nx
from gensim.models import Word2Vec

class DeepWalker(object):

    def __init__(self, graph, args):
        self.graph = graph
        self.args = args
        

    def small_walk(self,start_node):
        walk = [start_node]
        while len(walk) < self.args.walk_length:
            walk = walk + [random.sample(nx.neighbors(self.graph,walk[-1]),1)[0]]
            if len(nx.neighbors(self.graph,walk[-1])) ==0:
                break
        return walk

    def create_features(self):
        self.paths = []
        for node in tqdm(self.graph.nodes()):
            for k in range(self.args.number_of_walks):
                walk = self.small_walk(node)
                self.paths.append(walk)

    def learn_base_embedding(self):
        self.paths = [[str(node) for node in walk] for walk in self.paths]
        model = Word2Vec(self.paths, size = self.args.dimensions, window = self.args.window_size, min_count = 1, sg = 1, workers = self.args.workers, iter = 1)
        self.embedding = np.array([list(model[str(n)]) for n in self.graph.nodes()])
        return self.embedding
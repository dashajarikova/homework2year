import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora_1_300_10.vec.gz'#у меня работает только так, но сделаю строчку универсальную
#m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)

model.init_sims(replace=True)

gr={}
words = ['торт_NOUN', 'печенье_NOUN', 'булочка_NOUN', 'кекс_NOUN']
for word in words:
    if word in model:
        for i in model.most_similar(positive=[word], topn=10):
            if i[0] not in gr:
                gr[i[0]]=i[1]
    else:
        pass

G = nx.Graph()
for word in words:
    G.add_node(word, label = "word")
for el in gr:
    if gr[el]>0.5:
        G.add_node(el, label="el")
        G.add_edge(word, el)

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50)
nx.draw_networkx_edges(G, pos, edge_color='blue')
nx.draw_networkx_labels(G, pos, font_size=8, font_family='Arial')
plt.axis('off') 
plt.show()

print('Радиус графа: ', nx.radius(G))
print('Коэффициент кластеризации: ', nx.average_clustering(G))

deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print(nodeid)
    break

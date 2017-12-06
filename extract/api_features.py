import snap
import os
from scipy import stats
import numpy as np

package_names = {}
with open('extract/api_packages.txt') as f:
    for i, line in enumerate(f):
        package_names[i] = line.strip()


def maxIndegNode(G):
    node_centralities = [(node.GetId(), node.GetInDeg()) for node in G.Nodes() if node.GetId() in package_names]
    max_id = max(node_centralities, key = lambda x: x[1])[0]
    return package_names[max_id]
    # return max(node_centralities, key = lambda x: x[1])[1]


def maxClosenessNode(G):
    node_centralities = [(node.GetId(), snap.GetClosenessCentr(G, node.GetId(), True, False)) for node in G.Nodes() if node.GetId() in package_names]
    max_id = max(node_centralities, key = lambda x: x[1])[0]
    return package_names[max_id]
    # return max(node_centralities, key = lambda x: x[1])[1]


def test(family):
    path = 'data/' + family + '/'
    files = os.listdir(path)
    graph_files = filter(lambda x: '.apigraph' in x, files)
    maxindegs = []
    maxclosenesses = []

    # f = graph_files[0]
    # FIn = snap.TFIn(path + f)
    # G = snap.TNEANet.Load(FIn)
    # snap.DrawGViz(G, snap.gvlDot, family + '.png', family, True)

    for f in graph_files[:min(len(graph_files), 100) - 1]:
        FIn = snap.TFIn(path + f)
        G = snap.TNEANet.Load(FIn)
        if G.GetNodes() == 0 or G.GetEdges == 0:
            continue

        maxindegs.append(maxIndegNode(G))
        maxclosenesses.append(maxClosenessNode(G))

    print 'Indegree'
    print stats.mode(maxindegs)[0][0]
    # print np.mean(maxindegs)

    print 'Closeness'
    print stats.mode(maxclosenesses)[0][0]
    # print np.mean(maxclosenesses)
    print ''

def main():
    for family in os.listdir('data/graphs/'):
        if family == '.githold':
            continue
        print family
        test(family)


if __name__ == "__main__":
    main()

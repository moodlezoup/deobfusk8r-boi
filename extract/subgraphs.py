import snap
import random
import pprint
import os
import numpy as np


def getFilePaths(apiGraph=False):
    file_paths = []
    for family in os.listdir('data/graphs'):
        if family == '.githold':
            continue
        path = 'data/graphs/' + family + '/'
        all_files = os.listdir(path)
        if apiGraph:
            file_paths += [path + f for f in all_files if '.apigraph' in f]
        else:
            file_paths += [path + f for f in all_files if '.edges' in f]
    return file_paths



def estimate3SubgraphFrequencies(file_name, apiGraph=False):
    subgraph_counts = np.zeros(7)
    # 0 -> 0 edges
    # 1 -> 1 edge
    # 2 -> 2 edges to same node
    # 3 -> 2 edges from same node
    # 4 -> 2 edges though one node
    # 5 -> 3 edge cycle
    # 6 -> 3 edge, not cycle

    if apiGraph:
        FIn = snap.TFIn(file_name)
        Network = snap.TNEANet.Load(FIn)
        G = snap.ConvertGraph(snap.PNGraph, Network)
    else:
        G = snap.LoadEdgeList(snap.PNGraph, file_name, 0, 1)

    for _ in range(10000):
        sG = snap.GetRndSubGraph(G, 3)
        num_edges = sG.GetEdges()

        if num_edges == 0:
            subgraph_counts[0] += 1

        elif num_edges == 1:
            subgraph_counts[1] += 1

        elif num_edges == 2:
            max_indeg = sG.GetNI(snap.GetMxInDegNId(sG)).GetInDeg()
            max_outdeg = sG.GetNI(snap.GetMxOutDegNId(sG)).GetOutDeg()
            if max_indeg == 2:
                subgraph_counts[2] += 1
            elif max_outdeg == 2:
                subgraph_counts[3] += 1
            else:
                subgraph_counts[4] += 1

        else:
            max_indeg = sG.GetNI(snap.GetMxInDegNId(sG)).GetInDeg()
            if max_indeg == 1:
                subgraph_counts[5] += 1
            else:
                subgraph_counts[6] += 1

    subgraph_frequencies = subgraph_counts / sum(subgraph_counts)
    for freq in subgraph_frequencies:
        pretty = "%1.5f" % freq
        print pretty

def estimate4UndirectedSubgraphFrequencies(file_name, connected=True, apiGraph=False):
    subgraph_counts = np.zeros(10)
    # 0 -> 0 edges
    # 1 -> 1 edge
    # 2 -> 2 adjacent edges
    # 3 -> 2 non-adjacent edges
    # 4 -> 3-star
    # 5 -> 3-path
    # 6 -> tailed triangle
    # 7 -> 4-cycle
    # 8 -> chordal 4-cycle
    # 9 -> 4-clique

    if apiGraph:
        FIn = snap.TFIn(file_name)
        Network = snap.TNEANet.Load(FIn)
        G = snap.ConvertGraph(snap.PUNGraph, Network)
    else:
        G = snap.LoadEdgeList(snap.PUNGraph, file_name, 0, 1)

    for _ in range(100000):
        sG = snap.GetRndSubGraph(G, 4)
        num_edges = sG.GetEdges()
        if connected and num_edges < 3:
            continue

        if num_edges == 0:
            subgraph_counts[0] += 1

        elif num_edges == 1:
            subgraph_counts[1] += 1

        elif num_edges == 2:
            maxdeg = sG.GetNI(snap.GetMxDegNId(sG)).GetDeg()
            if maxdeg == 2:
                subgraph_counts[2] += 1
            else:
                subgraph_counts[3] += 1

        elif num_edges == 3:
            maxdeg = sG.GetNI(snap.GetMxDegNId(sG)).GetDeg()
            if maxdeg == 3:
                subgraph_counts[4] += 1
            else:
                subgraph_counts[5] += 1

        elif num_edges == 4:
            maxdeg = sG.GetNI(snap.GetMxDegNId(sG)).GetDeg()
            if maxdeg == 3:
                subgraph_counts[6] += 1
            else:
                subgraph_counts[7] += 1

        elif num_edges == 5:
            subgraph_counts[8] += 1

        else:
            subgraph_counts[9] += 1

    subgraph_frequencies = subgraph_counts / sum(subgraph_counts)
    for freq in subgraph_frequencies:
        pretty = "%1.4f" % freq
        print pretty


def main():
    file_paths = getFilePaths(apiGraph=True)
    # estimate3SubgraphFrequencies(file_paths[0], apiGraph=True)
    estimate4UndirectedSubgraphFrequencies(file_paths[0], connected=False, apiGraph=True)


if __name__ == "__main__":
    main()

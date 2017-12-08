import snap
import numpy as np


num_samples = 50000


def estimate3SubgraphFrequencies(Network):
    G = snap.ConvertGraph(snap.PNGraph, Network)

    subgraph_counts = np.zeros(7)
    # 0 -> 0 edges
    # 1 -> 1 edge
    # 2 -> 2 edges to same node
    # 3 -> 2 edges from same node
    # 4 -> 2 edges though one node
    # 5 -> 3 edge cycle
    # 6 -> 3 edge, not cycle

    for _ in range(num_samples):
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

    return list(subgraph_counts / sum(subgraph_counts))


def estimate4SubgraphFrequencies(Network, connected=True):
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

    G = snap.ConvertGraph(snap.PUNGraph, Network)

    for _ in range(num_samples):
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

    return list(subgraph_counts / sum(subgraph_counts))

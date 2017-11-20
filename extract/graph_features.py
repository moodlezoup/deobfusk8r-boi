# import argparse
import snap
import numpy as np
import pprint

# parser = argparse.ArgumentParser()
# parser.add_argument('--inputFile', '-i', required=True)
# args = parser.parse_args()
# G = snap.LoadEdgeList(snap.PNEANet, args.inputFile, 0, 1)

def avgIndegCentrality(G):
    centralities = np.zeros(G.GetNodes())
    for i, node in enumerate(G.Nodes()):
        centralities[i] = node.GetInDeg()
    # Weight
    centralities = centralities / float(max(centralities))
    # Avg
    return np.mean(centralities)

def avgOutdegCentrality(G):
    centralities = np.zeros(G.GetNodes())
    for i, node in enumerate(G.Nodes()):
        centralities[i] = node.GetOutDeg()
    # Weight
    centralities = centralities / float(max(centralities))
    # Avg
    return np.mean(centralities)

def avgBetweennessCentrality(G):
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    betweenness = snap.TFltV()
    snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
    Nodes.GetDatV(betweenness)
    betweenness = np.array(betweenness)
    betweenness = betweenness / float(max(betweenness))
    return np.mean(betweenness)

def avgClosenessCentrality(G):
    centralities = np.zeros(G.GetNodes())
    for i, node in enumerate(G.Nodes()):
        centralities[i] = snap.GetClosenessCentr(G, node.GetId(), True, True)
    centralities = centralities / float(max(centralities))
    return np.mean(centralities)

def numNodes(Network):
    return Network.GetNodes()

def numEdges(Network):
    return Network.GetEdges()

def numUniqueEdges(Network):
    return snap.CntUniqDirEdges(Network)

def numSelfLoops(Network):
    return snap.CntSelfEdges(Network)

def maxIndegree(Network):
    node_id = snap.GetMxInDegNId(Network)
    return Network.GetNI(node_id).GetInDeg()

def maxOutdegree(Network):
    node_id = snap.GetMxOutDegNId(Network)
    return Network.GetNI(node_id).GetOutDeg()

def numSccs(Network):
    sccs = snap.TCnComV()
    snap.GetSccs(Network, sccs)
    return len(sccs)

def effectiveDirDiameter(Network):
    return snap.GetBfsEffDiam(Network, 100, True)

def effectiveUndirDiameter(Network):
    return snap.GetBfsEffDiam(Network, 100, False)

def ratioIndeg1(Network):
    return snap.CntInDegNodes(Network, 1) / float(Network.GetNodes())

def ratioOutdeg1(Network):
    return snap.CntOutDegNodes(Network, 1) / float(Network.GetNodes())

def avgClustering(Network):
    return snap.GetClustCf(Network)

def ratioTriadEdges(Network):
    return snap.GetTriadEdges(Network) / float(Network.GetEdges())

def density(Network):
    return 2 * Network.GetEdges() / float(Network.GetNodes() * (Network.GetNodes() - 1))

extractors = {
    'num nodes': numNodes,
    'num edges': numEdges,
    'num unique edges': numUniqueEdges,
    'num self loops': numSelfLoops,
    'max indeg': maxIndegree,
    'max outdeg': maxOutdegree,
    'num sccs': numSccs,
    'eff dir diameter': effectiveDirDiameter,
    'eff undir diameter': effectiveUndirDiameter,
    'ratio indeg 1 nodes': ratioIndeg1,
    'ratio outdeg 1 nodes': ratioOutdeg1,
    'avg clustering': avgClustering,
    'ratio triad edges': ratioTriadEdges,
    'density': density,
    'avg indeg centrality': avgIndegCentrality,
    'avg outdeg centrality': avgOutdegCentrality,
    ## Expensive
    # 'avg betweeness centrality': avgBetweennessCentrality,
    'avg closeness centrality': avgClosenessCentrality,
}


# Degree distribution
# DegToCntV = snap.TIntPrV()
# snap.GetInDegCnt(Network, DegToCntV)
# snap.GetOutDegCnt(Network, DegToCntV)
# highest pagerank nodes
# highest indegree/oudegree nodes

# triad/subgraph frequency
# power law degree exponent
# HITS score

# Modularity of classes?
# Number of ingoing/outoing edges to specific functions/classes?

# network constraint measure

# network_features = getNetworkFeatures(Network, Directed, Undirected)
# pprint.pprint(network_features)

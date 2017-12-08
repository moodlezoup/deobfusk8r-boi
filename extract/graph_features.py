import snap
import numpy as np


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

def avgClosenessCentrality(G):
    centralities = np.zeros(G.GetNodes())
    for i, node in enumerate(G.Nodes()):
        centralities[i] = snap.GetClosenessCentr(G, node.GetId(), True, True)
    centralities = centralities / float(max(centralities))
    return np.mean(centralities)

def numNodes(G):
    return G.GetNodes()

def numEdges(G):
    return G.GetEdges()

def numUniqueEdges(G):
    return snap.CntUniqDirEdges(G)

def numSelfLoops(G):
    return snap.CntSelfEdges(G)

def maxIndegree(G):
    node_id = snap.GetMxInDegNId(G)
    return G.GetNI(node_id).GetInDeg()

def maxOutdegree(G):
    node_id = snap.GetMxOutDegNId(G)
    return G.GetNI(node_id).GetOutDeg()

def numSccs(G):
    sccs = snap.TCnComV()
    snap.GetSccs(G, sccs)
    return len(sccs)

def effectiveDirDiameter(G):
    return snap.GetBfsEffDiam(G, 100, True)

def effectiveUndirDiameter(G):
    return snap.GetBfsEffDiam(G, 100, False)

def ratioIndeg1(G):
    return snap.CntInDegNodes(G, 1) / float(G.GetNodes())

def ratioOutdeg1(G):
    return snap.CntOutDegNodes(G, 1) / float(G.GetNodes())

def avgClustering(G):
    return snap.GetClustCf(G)

def ratioTriadEdges(G):
    return snap.GetTriadEdges(G) / float(G.GetEdges())

def density(G):
    return 2 * G.GetEdges() / float(G.GetNodes() * (G.GetNodes() - 1))


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
    'avg closeness centrality': avgClosenessCentrality,
}

import numpy as np
import snap

def getNeighbors(G, nid):
    node = G.GetNI(nid)
    neighbors = set([node.GetNbrNId(i) for i in range(node.GetDeg())])
    return neighbors

def sortNodesByDeg(G):
    degrees = snap.TIntV()
    snap.GetDegSeqV(G, degrees)
    node_degrees = zip(range(len(degrees)), degrees)
    node_degrees.sort(key = lambda x: x[1], reverse=True)
    return node_degrees

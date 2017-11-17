import matplotlib.pyplot as plt
import numpy as np
import pprint
import snap
import os
import random
import graph_features

def sampleFeatures(family, feature, numSamples=500):
    path = 'data/' + family + '/'
    files = os.listdir(path)
    edge_files = filter(lambda x: '.edges' in x, files)
    random.shuffle(edge_files)
    features = np.zeros(numSamples)
    count = 0
    i = 0
    while count < numSamples:
        f = edge_files[i]
        i += 1
        G = snap.LoadEdgeList(snap.PNEANet, path + f, 0, 1)
        if G.GetEdges() == 0 or G.GetNodes() == 0:
            continue
        extractor = graph_features.extractors[feature]
        features[count] = extractor(G)
        count += 1
    return features

def avgFeature(family, feature, numSamples=200):
    features = sampleFeatures(family, feature, numSamples)
    return (np.mean(features), np.std(features))

def compareGraphFeature(families, feature):
    features = {f: avgFeature(f, feature) for f in families}
    pprint.pprint(features)
    # features = [avgFeature(f) for f in families]

# def plotGraphFeature(families, feature):
#     familyFeatures = {family: sampleFeatures(f, feature) for f in families}
    # for family, features in familyFeatures.items():


def avgDegreeDist(family, direction, numSamples=100):
    path = 'data/' + family + '/'
    files = os.listdir(path)
    edge_files = filter(lambda x: '.edges' in x, files)
    random.shuffle(edge_files)
    maxdeg = 0
    Gs = [snap.LoadEdgeList(snap.PNEANet, path + f, 0, 1) for f in edge_files[:numSamples]]
    if direction == 'in':
        maxdeg = max([G.GetNI((snap.GetMxInDegNId(G))).GetInDeg() for G in Gs])
    else:
        maxdeg = max([G.GetNI((snap.GetMxOutDegNId(G))).GetOutDeg() for G in Gs])

    avg_deg_dist = np.zeros(maxdeg + 1)
    for G in Gs:
        DegToCntV = snap.TIntPrV()
        if direction == 'in':
            snap.GetInDegCnt(G, DegToCntV)
        else:
            snap.GetOutDegCnt(G, DegToCntV)

        for item in DegToCntV:
            deg = item.GetVal1()
            avg_deg_dist[deg] += item.GetVal2()
    avg_deg_dist = avg_deg_dist / numSamples
    return avg_deg_dist

def plotDegreeDist(families, direction):
    dists = [avgDegreeDist(f, direction) for f in families]
    maxlen = max([len(dist) for dist in dists])
    for i, dist in enumerate(dists):
        if len(dist) < maxlen:
            dists[i] = np.pad(dist, (0, maxlen - len(dist)), 'constant')

    colors = {
        'Airpush': 'r',
        'Kuguo': 'b',
        'Dowgin': 'y',
        'DroidKungFu': 'm',
        'BankBot': 'c',
        'FakeInst': 'g',
    }

    for family, dist in zip(families, dists):
        clr = colors[family]
        plt.loglog(range(maxlen), dist, color = clr, label = family)

    if direction == 'in':
        plt.xlabel('In-Degree')
        plt.ylabel('In-Degree Distribution')
    else:
        plt.xlabel('Out-Degree')
        plt.ylabel('Out-Degree Distribution')

    plt.legend()
    plt.show()

def main():
    # plotDegreeDist(['Airpush', 'Kuguo', 'Dowgin', 'DroidKungFu', 'BankBot', 'FakeInst'], 'out')
    for feature in graph_features.extractors.keys():
        print feature
        compareGraphFeature(['Airpush', 'Kuguo', 'Dowgin', 'DroidKungFu', 'BankBot', 'FakeInst'], feature)

if __name__ == "__main__":
    main()

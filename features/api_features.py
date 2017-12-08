import snap


package_names = {}
with open('extract/api_packages.txt') as f:
    for i, line in enumerate(f):
        package_names[i] = line.strip()


def maxIndegNode(apiGraph):
    node_centralities = [(node.GetId(), node.GetInDeg()) for node in apiGraph.Nodes() if node.GetId() in package_names]
    max_id = max(node_centralities, key = lambda x: x[1])[0]
    return package_names[max_id]


def maxClosenessNode(apiGraph):
    node_centralities = [(node.GetId(), snap.GetClosenessCentr(apiGraph, node.GetId(), True, False)) for node in apiGraph.Nodes() if node.GetId() in package_names]
    max_id = max(node_centralities, key = lambda x: x[1])[0]
    return package_names[max_id]

import os
import snap
import multiprocessing


api_packages = set()
package_ids = {}
with open('extract/api_packages.txt') as f:
    for i, line in enumerate(f):
        api_packages.add(line.strip())
        package_ids[line.strip()] = i


def getFileNames():
    file_names = []
    for family in os.listdir('data/graphs'):
        if family == '.githold':
            continue
        path = 'data/graphs' + family + '/'
        all_files = os.listdir(path)
        file_names += [path + f.split('.')[0] for f in all_files if '.edges' in f]
    return file_names


def genApiGraph(file_name):
    key_file = file_name + '.key'
    edge_file = file_name + '.edges'

    node_to_package = {}
    packages_that_appear = set()
    with open(key_file, 'r') as f:
        for line in f:
            nid = line.split(' ')[0]
            full_path = line.split(' ')[1][1:-1]
            api_package = '.'.join(full_path.split('.')[:-1])
            if api_package in api_packages:
                node_to_package[nid] = package_ids[api_package]
                packages_that_appear.add(api_package)
            else:
                if full_path not in package_ids:
                    package_ids[full_path] = len(package_ids)
                    packages_that_appear.add(full_path)
                node_to_package[nid] = package_ids[full_path]

    api_graph = snap.TNEANet.New()
    for package, i in package_ids.items():
        # if package in packages_that_appear:
        api_graph.AddNode(i)

    with open(edge_file, 'r') as f:
        for line in f:
            u, v = line.strip().split(' ')
            api_graph.AddEdge(node_to_package[u], node_to_package[v])

    FOut = snap.TFOut(file_name + '.apigraph')
    api_graph.Save(FOut)
    FOut.Flush()


def main():
    file_names = getFileNames()
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(genApiGraph, file_names)


if __name__ == "__main__":
    main()

from sqlitedict import SqliteDict
import sklearn.model_selection as model_selection
import graph_features
import api_features
import subgraph_features
import json
import os
import snap
import multiprocessing


db_path = 'data/processed/data.sqlite'

family_types = json.load(open('extract/family_types.json'))


def splitData(d):
    for category, files in d.items():
        train, test = model_selection.train_test_split(files, test_size=0.3, random_state=420)
        d[category] = {'train': train, 'test': test}


def processFileNames():
    global all_files
    global files_by_family
    global files_by_type
    global files_by_type2

    all_files = []
    files_by_family = {}
    files_by_type = {}
    files_by_type2 = {}

    for family in os.listdir('data/graphs'):
        if family == '.githold':
            continue
        path = 'data/graphs/' + family + '/'

        files = os.listdir(path)
        file_names = [path + f.split('.')[0] for f in files if '.edges' in f]
        all_files += file_names
        files_by_family[family] = file_names

        family_type = family_types[family]
        if family_type in files_by_type:
            files_by_type[family_type] += file_names
        else:
            files_by_type[family_type] = file_names

        family_type2 = 'Trojan' if 'Trojan' in family_type else family_type
        if family_type2 in files_by_type2:
            files_by_type2[family_type2] += file_names
        else:
            files_by_type2[family_type2] = file_names



def extractSubgraphFeatures(features, G, apiG):
    def freqFeature(prefix, frequencies):
        for i, freq in enumerate(frequencies):
            features[prefix + ' ' + str(i)] = freq

    # threeSubgraphsFreqsG = subgraph_features.estimate3SubgraphFrequencies(G)
    threeSubgraphsFreqsApi = subgraph_features.estimate3SubgraphFrequencies(apiG)
    # freqFeature('G 3-subgraph', threeSubgraphsFreqsG)
    freqFeature('Api 3-subgraph', threeSubgraphsFreqsApi)

    # Weight the less frequent subgraphs more heavily
    # fourSubgraphsFreqsG = subgraph_features.estimate4SubgraphFrequencies(G)[:4]
    fourSubgraphsFreqsApi = subgraph_features.estimate4SubgraphFrequencies(apiG)[:4]
    # fourSubgraphsFreqsG += subgraph_features.estimate4SubgraphFrequencies(G, connected=False)[4:]
    fourSubgraphsFreqsApi += subgraph_features.estimate4SubgraphFrequencies(apiG, connected=False)[4:]
    # freqFeature('G 4-subgraph', fourSubgraphsFreqsG)
    freqFeature('Api 4-subgraph', fourSubgraphsFreqsApi)


def extract(f):
    print f
    # print 'Loading graphs...'
    file_name = f.split('/')[-1]
    family = f.split('/')[2]
    G = snap.LoadEdgeList(snap.PNEANet, f + '.edges', 0, 1)
    apiG = snap.LoadEdgeList(snap.PNEANet, f + '.apigraph', 0, 1)

    features = {}
    for feature, extractor in graph_features.extractors.items():
        # print feature
        features[feature] = extractor(G)
        features['api_' + feature] = extractor(apiG)

    # print 'Api features'
    features['max indeg node'] = api_features.maxIndegNode(apiG)
    features['max closeness node'] = api_features.maxClosenessNode(apiG)

    # print 'Subgraph features'
    extractSubgraphFeatures(features, G, apiG)
    sqlite_db[file_name] = features



def extractAll():
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(extract, all_files)


def main():
    print 'Processing file names...'
    processFileNames()

    print 'Splitting data...'
    for d in [files_by_family, files_by_type, files_by_type2]:
        splitData(d)

    global sqlite_db
    sqlite_db = SqliteDict(db_path, autocommit=True)
    sqlite_db['files_by_family'] = files_by_family
    sqlite_db['files_by_type'] = files_by_type
    sqlite_db['files_by_type2'] = files_by_type2

    print 'Extracting...'
    extractAll()

    sqlite_db.close()


if __name__ == "__main__":
    main()

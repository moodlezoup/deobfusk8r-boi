from sqlitedict import SqliteDict
import sklearn.model_selection as model_selection
import graph_features
import api_features
import subgraph_features
import json


db_path = 'data/processed/data.sqlite'

family_types = json.load(open('data/family_types.json'))
all_files = []
files_by_family = {}
files_by_type = {}
files_by_type2 = {}


def splitData(d):
    for category, files in d.items():
        train, test = model_selection.train_test_split(files, test_size=0.3, random_state=420)
        d[category] = {'train': train, 'test': test}


def processFileNames():
    for family in os.listdir('data/graphs'):
        if family == '.githold':
            continue
        path = 'data/graphs/' + family + '/'

        files = os.listdir(path)
        all_files += files
        file_names = [path + f.split('.')[0] for f in files if '.edges' in f]
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
            features[prefix + ' ' + i] = freq

    threeSubgraphsFreqsG = subgraph_features.estimate3SubgraphFrequencies(G)
    threeSubgraphsFreqsApi = subgraph_features.estimate3SubgraphFrequencies(apiG)
    freqFeature('G 3-subgraph', threeSubgraphsFreqsG)
    freqFeature('Api 3-subgraph', threeSubgraphsFreqsApi)

    # Weight the less frequent subgraphs more heavily
    fourSubgraphsFreqsG = subgraph_features.estimate4SubgraphFrequencies(G)[:4]
    fourSubgraphsFreqsApi = subgraph_features.estimate4SubgraphFrequencies(apiG)[:4]
    fourSubgraphsFreqsG += subgraph_features.estimate4SubgraphFrequencies(G, connected=False)[4:]
    fourSubgraphsFreqsApi += subgraph_features.estimate4SubgraphFrequencies(apiG, connected=False)[4:]
    freqFeature('G 4-subgraph', fourSubgraphsFreqsG)
    freqFeature('Api 4-subgraph', fourSubgraphsFreqsApi)


def extractAll(db):
    for f in all_files:
        file_name = f.split('/')[-1]
        family = f.split('/')[2]
        G = snap.LoadEdgeList(snap.PNEANet, f + '.edges', 0, 1)
        FIn = snap.TFIn(f + '.apigraph')
        apiG = snap.TNEANet.Load(FIn)

        features = {}
        for feature, extractor in graph_features.extractors.items():
            features[feature] = extractor(G)
            features['api_' + feature] = extractor(apiG)

        features['max indeg node'] = api_features.maxIndegNode(apiG)
        features['max closeness node'] = api_features.maxClosenessNode(apiG)

        extractSubgraphFeatures(features, G, apiG)
        db[file_name] = features


def main():
    print 'Processing file names...'
    processFileNames()

    print 'Splitting data...'
    for d in [files_by_family, files_by_type, files_by_type2]:
        splitData(d)


    sqlite_db = SqliteDict(db_path, autocommit=True)
    sqlite_db['files_by_family'] = files_by_family
    sqlite_db['files_by_type'] = files_by_type
    sqlite_db['files_by_type2'] = files_by_type2

    print 'Extracting...'
    extractAll(sqlite_db)

    sqlite_db.close()


if __name__ == "__main__":
    main()

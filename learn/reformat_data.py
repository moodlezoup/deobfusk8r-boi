from sqlitedict import SqliteDict
from sklearn.feature_extraction import DictVectorizer


db_path = 'data/processed/data.sqlite'
sqlite_db = SqliteDict(db_path, autocommit=True)


def filteredFamilies():
    train_x = []
    train_y = []
    test_x = []
    test_y = []

    for classification, files in sqlite_db[grouping].items():
        for file_name in files['train']:
            if file_name in sqlite_db:
                features = sqlite_db[file_name]
                train_x.append(features)
                train_y.append(classification)
        for file_name in files['test']:
            if file_name in sqlite_db:
                features = sqlite_db[file_name]
                test_x.append(features)
                test_y.append(classification)

    sqlite_db['files_by_family2 train_x'] = train_x
    sqlite_db[grouping + ' train_y'] = train_y
    sqlite_db[grouping + ' test_x'] = test_x
    sqlite_db[grouping + ' test_y'] = test_y


def reformat(grouping):
    train_x = []
    train_y = []
    test_x = []
    test_y = []

    table = sqlite_db['files_by_family'] if grouping == 'files_by_family2' else sqlite_db[grouping]
    for classification, files in table.items():
        if grouping == 'files_by_family2':
            if len(files['train']) + len(files['test']) < 2000:
                continue

        for file_name in files['train']:
            if file_name in sqlite_db:
                features = sqlite_db[file_name]
                train_x.append(features)
                train_y.append(classification)
        for file_name in files['test']:
            if file_name in sqlite_db:
                features = sqlite_db[file_name]
                test_x.append(features)
                test_y.append(classification)

    sqlite_db[grouping + ' train_x'] = train_x
    sqlite_db[grouping + ' train_y'] = train_y
    sqlite_db[grouping + ' test_x'] = test_x
    sqlite_db[grouping + ' test_y'] = test_y


# reformat('files_by_family')
reformat('files_by_family2')
# reformat('files_by_type')
# reformat('files_by_type2')


def vectorize(vectorizer, grouping):
    sqlite_db[grouping + ' train_x_vectorized'] = vectorizer.transform(sqlite_db[grouping + ' train_x'])
    sqlite_db[grouping + ' test_x_vectorized'] = vectorizer.transform(sqlite_db[grouping + ' test_x'])


# vectorizer = DictVectorizer(sparse=False)
# vectorizer.fit(sqlite_db['files_by_family train_x'])
# sqlite_db['vectorizer'] = vectorizer
vectorizer = sqlite_db['vectorizer']

# vectorize(vectorizer, 'files_by_family')
vectorize(vectorizer, 'files_by_family2')
# vectorize(vectorizer, 'files_by_type')
# vectorize(vectorizer, 'files_by_type2')


sqlite_db.close()

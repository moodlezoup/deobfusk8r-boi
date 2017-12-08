from sklearn.linear_model import SGDClassifier
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection
from sklearn.pipeline import Pipeline
from sqlitedict import SqliteDict
from pprint import pprint
from time import time
import logging
from sklearn.svm import SVC

db_path = 'data/processed/data.sqlite'

def generateClassifier(grouping):
    with SqliteDict(db_path, autocommit=True) as sqlite_db:
        X = sqlite_db[grouping + ' train_x_vectorized']
        Y = sqlite_db[grouping + ' train_y']

        clf = SGDClassifier(n_jobs=-1)
        print '=========== Train ==========='
        predictions = model_selection.cross_val_predict(clf, X, Y, cv=5)
        print metrics.classification_report(Y, predictions)
        print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))
        print '============================='
        # clf.fit(X, Y)
        #
        # print '=========== Test ============'
        # X = sqlite_db[grouping + ' test_x_vectorized']
        # Y = sqlite_db[grouping + ' test_y']
        # predictions = clf.predict(X)
        # print metrics.classification_report(Y, predictions)
        # print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))
        # print '============================='

        # print 'saving classifier'
        # sqlite_db['classifier'] = clf


def parameterTuning(grouping):
    # pipeline = Pipeline([
    #     ('clf', SVC()),
    # ])
    # params = [
    #   {'clf__C': [0.1], 'clf__kernel': ['linear']},
    #   # {'clf__C': [0.1, 1, 10, 100, 1000], 'clf__kernel': ['rbf', 'sigmoid']},
    #   # {'clf__C': [0.1, 1, 10, 100, 1000], 'clf__degree': [2, 3, 4], 'clf__kernel': ['poly'] }
    # ]
    pipeline = Pipeline([
        ('clf', SGDClassifier(n_jobs=-1)),
    ])
    params = [
      {'clf__penalty': ['l1', 'l2', 'elasticnet'], 'clf__loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']}
    ]

    sqlite_db = SqliteDict(db_path, autocommit=True)
    X = sqlite_db[grouping + ' train_x_vectorized']
    Y = sqlite_db[grouping + ' train_y']

    grid_search = model_selection.GridSearchCV(pipeline, param_grid=params, n_jobs=-1, verbose=1)
    t0 = time()
    grid_search.fit(X, Y)
    print("done in %0.3fs" % (time() - t0))
    sqlite_db['grid_search'] = grid_search
    sqlite_db.close()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in params[0].keys():
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    predictions = grid_search.best_estimator_.predict(X)
    print metrics.classification_report(Y, predictions)
    # print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))


if __name__ == "__main__":
    print 'learning'
    parameterTuning('files_by_type2')
    # generateClassifier('files_by_family')

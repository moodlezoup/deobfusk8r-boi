from sklearn.linear_model import SGDClassifier
import sklearn.metrics as metrics
import sklearn.model_selection as model_selection
from sklearn.pipeline import Pipeline
from sqlitedict import SqliteDict
from pprint import pprint
from time import time
import logging
from sklearn.svm import SVC


# sci-kit learn classifiers
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


from xgboost import XGBClassifier
# from sklearn.preprocessing import LabelEncoder


db_path = 'data/processed/data.sqlite'

def generateClassifier(grouping, clf=KNeighborsClassifier(3)):
    with SqliteDict(db_path, autocommit=True) as sqlite_db:
        X = sqlite_db[grouping + ' train_x_vectorized']
        Y = sqlite_db[grouping + ' train_y']

        # clf = KNeighborsClassifier(n_neighbors=6, weights='distance', p=1, n_jobs=-1)
        # clf = XGBClassifier(max_depth=4, learning_rate=0.1, n_estimators=100, objective='multi:softprob')
        clf = ExtraTreesClassifier(criterion='entropy', max_features=0.7)
        # clf = RandomForestClassifier()
        # clf = DecisionTreeClassifier()

        # print '=========== Train ==========='
        # predictions = model_selection.cross_val_predict(clf, X, Y, cv=5)
        # print metrics.classification_report(Y, predictions)
        # print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))
        # print '============================='

        clf.fit(X, Y)
        vectorizer = sqlite_db['vectorizer']
        feature_names = vectorizer.get_feature_names()
        feature_importances = clf.feature_importances_

        for (name, importance) in sorted(zip(feature_names, feature_importances), key = lambda x: x[1], reverse=True):
            print name, importance

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
        ('clf', ExtraTreesClassifier(n_jobs=-1)),
    ])
    params = [{
        'clf__n_estimators': [8, 10, 12],
        'clf__criterion': ['gini', 'entropy'],
        'clf__max_features': [0.4, 0.7, 1],
        'clf__class_weight': [None, 'balanced'],
    }]

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


def XGBoostClassifier(grouping):
    pipeline = Pipeline([
        ('clf', XGBClassifier(nthread=4)),
    ])
    params = [{
        'clf__max_depth': [4],
        'clf__learning_rate': [0.1],
        'clf__n_estimators': [100],
        'clf__objective': ['multi:softprob'],
    }]

    with SqliteDict(db_path, autocommit=True) as sqlite_db:
        X = sqlite_db[grouping + ' train_x_vectorized']
        Y = sqlite_db[grouping + ' train_y']

        grid_search = model_selection.GridSearchCV(pipeline, param_grid=params, n_jobs=-1, verbose=1)
        t0 = time()
        grid_search.fit(X, Y)
        print("done in %0.3fs" % (time() - t0))
        # sqlite_db['grid_search'] = grid_search
        # sqlite_db.close()

        print("Best score: %0.3f" % grid_search.best_score_)
        print("Best parameters set:")
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in params[0].keys():
            print("\t%s: %r" % (param_name, best_parameters[param_name]))

        predictions = grid_search.best_estimator_.predict(X)
        print metrics.classification_report(Y, predictions)

    # with SqliteDict(db_path, autocommit=True) as sqlite_db:
    #     X = sqlite_db[grouping + ' train_x_vectorized']
    #     Y = sqlite_db[grouping + ' train_y']
    #     clf = XGBClassifier(nthread=4)
    #     # model.fit(X, Y)
    #
    #     print '=========== Train ==========='
    #     predictions = model_selection.cross_val_predict(clf, X, Y, cv=5)
    #     print metrics.classification_report(Y, predictions)
    #     print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))
    #     print '============================='


if __name__ == "__main__":
    print 'learning'
    # XGBoostClassifier('files_by_type2')
    # parameterTuning('files_by_type2')
    generateClassifier('files_by_family2')
    # tryManyThings('files_by_family')

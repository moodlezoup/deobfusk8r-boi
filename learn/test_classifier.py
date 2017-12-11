import sklearn.metrics as metrics
from sqlitedict import SqliteDict
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import ExtraTreesClassifier
import itertools
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb


db_path = 'data/processed/data.sqlite'


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def fixFeatureName(name):
    return name.replace('Api', '(API)').replace('api_', '(API) ')

def getColor(name):
    if '(API)' in name:
        if 'subgraph' in name:
            return 'b'
        else:
            return 'r'
    else:
        return 'g'


def testClassifier(grouping):
        with SqliteDict(db_path, autocommit=True) as sqlite_db:
            X = sqlite_db[grouping + ' train_x_vectorized']
            Y = sqlite_db[grouping + ' train_y']

            clf = sqlite_db[grouping + ' classifier']
            # print '=========== Test ============'
            # X = sqlite_db[grouping + ' test_x_vectorized']
            # Y = sqlite_db[grouping + ' test_y']
            # predictions = clf.predict(X)
            # print metrics.classification_report(Y, predictions)
            # print "Accuracy: " + str(metrics.accuracy_score(Y, predictions))
            # print '============================='

            clf.fit(X, Y)
            vectorizer = sqlite_db['vectorizer']
            feature_names = vectorizer.get_feature_names()
            feature_importances = clf.feature_importances_

            sorted_features = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)[:20]
            sorted_importances = [feature[1] for feature in sorted_features]
            sorted_names = [fixFeatureName(feature[0]) for feature in sorted_features]
            sorted_colors = [getColor(name) for name in sorted_names]

            fig = plt.figure()
            ax = fig.add_subplot(111)
            bars = ax.bar(range(len(sorted_features)), sorted_importances, width=0.7, align="center", color=sorted_colors)
            ax.set_ylabel('Normalized importance')
            ax.set_xticks(range(len(sorted_names)))
            ax.set_xticklabels(sorted_names, rotation=45, ha='right')
            plt.show()

            # cnf_matrix = confusion_matrix(Y, predictions)
            # np.set_printoptions(precision=2)
            #
            # class_names = ['Airpush', 'Andup', 'Boxer', 'Dowgin', 'FakeInst', 'Koler']
            # # Plot non-normalized confusion matrix
            # plt.figure()
            # plot_confusion_matrix(cnf_matrix, classes=class_names, title='Confusion matrix, without normalization')
            #
            # # Plot normalized confusion matrix
            # plt.figure()
            # plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True, title='Normalized confusion matrix')
            # plt.show()

            # for (name, importance) in sorted(zip(feature_names, feature_importances), key = lambda x: x[1], reverse=True)[:10]:
            #     print name, importance


if __name__ == "__main__":
    testClassifier('files_by_family2')

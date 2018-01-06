"""
In this example the use of ActiveLearner is demonstrated on the iris dataset in a pool-based sampling setting.
For more information on the iris dataset, see https://en.wikipedia.org/wiki/Iris_flower_data_set
For its scikit-learn interface, see http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from modAL.models import ActiveLearner

# loading the iris dataset
iris = load_iris()

# initial training data
train_idx = [0, 50, 100]
X_train = iris['data'][train_idx]
y_train = iris['target'][train_idx]

# generating the pool
X_pool = np.delete(iris['data'], train_idx, axis=0)
y_pool = np.delete(iris['target'], train_idx)

# initializing the active learner
learner = ActiveLearner(
    predictor=KNeighborsClassifier(n_neighbors=3),
    X_initial=X_train, y_initial=y_train
)

# pool-based sampling
n_queries = 20
for idx in range(n_queries):
    query_idx, query_instance = learner.query(X_pool)
    learner.teach(
        X=X_pool[query_idx].reshape(1, -1),
        y=y_pool[query_idx].reshape(1, )
    )
    # remove queried instance from pool
    X_pool = np.delete(X_pool, query_idx, axis=0)
    y_pool = np.delete(y_pool, query_idx)

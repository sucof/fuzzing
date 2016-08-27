import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import numpy as np
import itertools

from sklearn.datasets import make_classification

from unbalanced_dataset import UnderSampler


def undersampling(x, y):
    verbose = False
    
    US = UnderSampler(verbose=verbose)
    usx, usy = US.fit_transform(x, y)

    return (usx, usy)


if __name__ == '__main__':
    
    x, y = make_classification(n_classes=2, class_sep=2, weights=[0.1, 0.9],
                           n_informative=3, n_redundant=1, flip_y=0,
                           n_features=20, n_clusters_per_class=1,
                           n_samples=1000, random_state=10)

    print type(x[0])
    undersampling(x, y)

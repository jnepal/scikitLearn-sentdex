import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs

centers = [[1, 1], [5, 5], [3, 10]]

X, y = make_blobs(n_samples = 500, centers = centers, cluster_std = 1)

plt.scatter(X[:, 0], X[:, 1])
plt.show()

ms = MeanShift()
ms.fit(X)
labels = ms.labels_

clusterCenters = ms.cluster_centers_

print(clusterCenters)
nClusters = len(np.unique(labels))

print("No of estimated clusters", nClusters)

colors = 10*["r.", "g.", "b.", "c.", "k.", "y.", "m."]

print(colors)
print(labels)

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

plt.scatter(clusterCenters[:, 0], clusterCenters[:, 1],
            marker = "x",
            s = 150,
            linewidths = 5,
            zorder = 10)
plt.show()
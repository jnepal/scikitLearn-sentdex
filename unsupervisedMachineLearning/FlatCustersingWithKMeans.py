import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

'''Matplot lib style'''
matplotlib.style.use('ggplot')

x = [1 , 5, 1.5, 8, 1, 9]
y = [2, 8, 1.8, 8, 0.6, 11]

plt.scatter(x, y)
plt.show()

X = np.array([[1, 2],
              [5, 8],
              [1.5, 1.8],
              [8, 8],
              [1, 0.6],
              [9, 11]])

kmeans = KMeans(n_clusters=2)
kmeans.fit(X)


centriods =  kmeans.cluster_centers_
labels = kmeans.labels_

print(centriods)
print(labels)

''' Graphing Purpose '''
colors = ["g.", "r."]

for i in range(len(X)):
    print("cordinate :", X[i], "label :", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

plt.scatter(centriods[:, 0], centriods[:, 1], marker = "x", s = 150, linewidths = 5, zorder = 10)
plt.show()


import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from sklearn import svm

#Matplot lib style
matplotlib.style.use("ggplot")

x = [1,5,1.5,8,1,9]
y = [2,8,1.8,8,0.6,11]

plt.scatter(x, y)
plt.show()

#Feature array of two features x and y
X = np.array([[1,2],
             [5,8],
             [1.5,1.8],
             [8,8],
             [1,0.6],
             [9,11]])


#label
#assigning 1 for higher values of cordinates like (5,8) and 0 for lower values of cordinates like [1,2]
y = [0,1,0,1,0,1]

#svm classifier
clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X, y)

#prediction
print(clf.predict([2,3])) #should give 0
print(clf.predict([5,5])) #should give 1

#coefficient
#coef_[] is only available for linear SVC
w = clf.coef_[0]
print(w)

#learning rate
a = -w[0] / w[1]

#Min element in feature is 0 and Max is 12
xx = np.linspace(0, 12)
yy = a * xx - clf.intercept_[0] / w[1]

#k- represents black solid line
h0 = plt.plot(xx, yy, 'k-', label="non weighted division")

#X[:, 0] is list of first element of feature numpy ordered pair X i.e [1,5,1.5,8,1,9]
#X[:, 1] is list of second element of feature numpy ordered pair X i.e [2,8,1.8,8,0.6,11]
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.legend()
plt.show()
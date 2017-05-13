import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

#digits data sets
digits = datasets.load_digits()

# print(digits.data)
# print(digits.target)
# print

#setting up classifier
clf = svm.SVC(gamma=0.0001, C=100)
x, y = digits.data[:-10], digits.target[:-10]
clf.fit(x, y)

print('Prediction :', clf.predict(digits.data[-2]))
plt.imshow(digits.images[-2], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()
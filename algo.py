import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn import svm

# Load data
X = []
y = []

for i in range(1, 101):
    fresh_img = cv2.imread(f'fresh_{i}.jpg')
    rotten_img = cv2.imread(f'rotten_{i}.jpg')
    X.append(cv2.cvtColor(fresh_img, cv2.COLOR_BGR2GRAY).flatten())
    y.append(0)
    X.append(cv2.cvtColor(rotten_img, cv2.COLOR_BGR2GRAY).flatten())
    y.append(1)

X = np.array(X)
y = np.array(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train SVM model
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# Test SVM model
y_pred = clf.predict(X_test)
accuracy = clf.score(X_test, y_test)

print(f'Accuracy: {accuracy}')

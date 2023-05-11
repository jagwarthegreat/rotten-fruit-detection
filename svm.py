import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import os

# Define the classes and their corresponding labels
classes = {'fresh_durian': 0, 'fresh_mango': 1, 'fresh_atis': 2, 'fresh_papaya': 3, 'rotten_durian': 4, 'rotten_mango': 5, 'rotten_atis': 6, 'rotten_papaya': 7, 'rotten_jackfruit': 8}

# Define the color ranges for fresh and rotten fruits
colors = {'fresh': [(25, 50, 50), (85, 255, 255)], 'rotten': [(0, 50, 50), (20, 255, 255)]}

# Define a function to extract features from an image using histogram of oriented gradients (HOG)
def extract_features(img):
    hog = cv2.HOGDescriptor((64,64), (16,16), (8,8), (8,8), 9)
    hist = hog.compute(img)
    return hist.flatten()

# Load the trained classifier
clf = SVC(kernel='linear', C=1.0, random_state=42)
clf = joblib.load('C:\\Python\\Fruit Grading System\\model\\classifier.joblib')

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_size = 1000 # minimum size of the bounding box (in pixels)

    # Detect fruits in the frame
    for cls, label in classes.items():
        if not cls.startswith('fresh'):
            continue
        mask = cv2.inRange(hsv, colors['fresh'][0], colors['fresh'][1])
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:
                continue
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            x, y, w, h = cv2.boundingRect(contour)
            fruit_img = frame[y:y + h, x:x + w]
            fruit_img = cv2.resize(fruit_img, (64, 64))
            features = extract_features(fruit_img)
            prediction = clf.predict([features])[0]
            if prediction == label:
                # Get the freshness percentage
                freshness = 100 - (area / (w * h)) * 100
                # Add the freshness percentage to the bounding box label
                label = '{} ({:.2f}%)'.format(cls.split('_')[1], freshness)
                # Draw the rotated bounding box and label on the frame
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_size:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            if w * h < min_size:
                continue
            fruit_img = frame[y:y + h, x:x + w]
            fruit_img = cv2.resize(fruit_img, (64, 64))
            features = extract_features(fruit_img)
            prediction = clf.predict([features])[0]
            if prediction == label:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, cls.split('_')[1], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_size:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            fruit_img = frame[y:y+h, x:x+w]
            fruit_img = cv2.resize(fruit_img, (64, 64))
            features = extract_features(fruit_img)
            prediction = clf.predict([features])[0]
            if prediction == label:
                # Get the freshness percentage
                freshness = 100 - (area / (w * h)) * 100
                # Add the freshness percentage to the bounding box label
                label = '{} ({:.2f}%)'.format(cls.split('_')[1], freshness)
                # Draw the bounding box and label on the frame
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)





    # Show the frame
    cv2.imshow('Fruit Grading System', frame)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

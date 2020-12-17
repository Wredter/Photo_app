import cv2

import numpy as np

face_detector = cv2.CascadeClassifier('xml_detectors\\haarcascades\\haarcascade_frontalface_default.xml')
eye_detector_1 = cv2.CascadeClassifier('xml_detectors\\haarcascades\\haarcascade_eye_tree_eyeglasses.xml')
eye_detector_2 = cv2.CascadeClassifier('xml_detectors\\haarcascades\\haarcascade_eye.xml')
eye_detector_3 = cv2.CascadeClassifier('xml_detectors\\haarcascades\\haarcascade_lefteye_2splits.xml')
smile_detector = cv2.CascadeClassifier('xml_detectors\\haarcascades\\haarcascade_smile.xml')

img_open = cv2.imread('Data\\IMG_20201217_184415.jpg', cv2.IMREAD_UNCHANGED)
img_closed = cv2.imread('Data\\IMG_20201216_185903.jpg', cv2.IMREAD_UNCHANGED)

img = img_open
eye_detector = eye_detector_1

print("Size : ", img.shape)
scale_percent = 600 / img.shape[1]
n_width = int(img.shape[1] * scale_percent)
n_heigh = int(img.shape[0] * scale_percent)
n_dim = (n_width, n_heigh)

resized_img = cv2.resize(img, n_dim, interpolation=cv2.INTER_AREA)

print("New Size : ", resized_img.shape)

cv2.imshow("Resized", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
print("Begining Detection")
face = face_detector.detectMultiScale(gray_img, 1.2, 5)
print("Ending Detection")
if face is ():
    print("NO FACE DETECTED")

for (x, y, w, h) in face:
    cv2.rectangle(resized_img, (x, y), (x + w, y + h), (127, 0, 255), 2)
    roi_grey = gray_img[y:y+h, x:x+w]
    roi_color = resized_img[y:y+h, x:x+w]
    eyes = eye_detector.detectMultiScale(roi_grey, 1.05, 4)
    smile = smile_detector.detectMultiScale(roi_grey, 1.2, 6)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    for (sx, sy, sw, sh) in smile:
        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 255, 20), 2)

cv2.imshow('Face Detection', resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

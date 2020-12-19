import cv2
import itertools as it
import numpy as np
from Tools import save_json
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="path", help="Provide PATH to photo")
import pathlib
pathlib.Path(__file__).parent.absolute()
face_detector = cv2.CascadeClassifier('./xml_detectors/haarcascades/haarcascade_frontalface_default.xml')
eye_detector_1 = cv2.CascadeClassifier('./xml_detectors/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
eye_detector_2 = cv2.CascadeClassifier('./xml_detectors/haarcascades/haarcascade_eye.xml')
eye_detector_3 = cv2.CascadeClassifier('./xml_detectors/haarcascades/haarcascade_lefteye_2splits.xml')
smile_detector = cv2.CascadeClassifier('./xml_detectors/haarcascades/haarcascade_smile.xml')
args = parser.parse_args()
img_path = args.path
img_open = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
# img_open2 = cv2.imread('Data\\CV_photo.jpg', cv2.IMREAD_UNCHANGED)
# img_closed = cv2.imread('Data\\IMG_20201216_185903.jpg', cv2.IMREAD_UNCHANGED)


img = img_open
eye_detector = eye_detector_2
Face = False
Eyes = False
Smile = False

print("Size : ", img.shape)
scale_percent = 600 / img.shape[1]
n_width = int(img.shape[1] * scale_percent)
n_heigh = int(img.shape[0] * scale_percent)
n_dim = (n_width, n_heigh)

resized_img = cv2.resize(img, n_dim, interpolation=cv2.INTER_AREA)

print("New Size : ", resized_img.shape)

# cv2.imshow("Resized", resized_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
print("Begining Detection")
face = face_detector.detectMultiScale(gray_img, 1.2, 5)
print("Ending Detection")
if len(face) is not 1:
    save_json(Face, Eyes, Smile)
    print("NO FACE DETECTED")
    exit(0)


for (x, y, w, h) in face:
    Face = True
    cv2.rectangle(resized_img, (x, y), (x + w, y + h), (127, 0, 255), 2)
    roi_grey = gray_img[y:y+h, x:x+w]
    roi_color = resized_img[y:y+h, x:x+w]
    eyes = eye_detector.detectMultiScale(roi_grey, 1.05, 4, minSize=(30, 30))
    smiles = smile_detector.detectMultiScale(roi_grey, 1.2, 6, minSize=(30, 60))
    remove = []
    if len(eyes) < 2:
        save_json(Face, Eyes, Smile)
        exit(0)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        if ey + (eh/2) > (h/2):
            remove.append(False)
        else:
            remove.append(True)
    eyes = list(it.compress(eyes, remove))
    eye_pairs = list(it.combinations(eyes, 2))
    remove = []
    if len(eyes) < 2:
        save_json(Face, Eyes, Smile)
        exit(0)
    for (eye_1, eye_2) in eye_pairs:
        # print(f"[{eye_1}, {eye_2}]")
        eye_variance = eye_1[3] * 0.15
        if eye_2[1] < eye_1[1] - eye_variance or eye_2[1] > eye_1[1] + eye_variance:
            remove.append(False)
        else:
            remove.append(True)
    eye_pairs = list(it.compress(eye_pairs, remove))
    if len(eye_pairs) is 1:
        Eyes = True
        center_min = min(eye_pairs[0][0][0]+(eye_pairs[0][0][2]/2), eye_pairs[0][1][0]+(eye_pairs[0][1][2]/2))
        center_max = max(eye_pairs[0][0][0] + (eye_pairs[0][0][2] / 2), eye_pairs[0][1][0] + (eye_pairs[0][1][2] / 2))
    else:
        save_json(Face, Eyes, Smile)
        exit(0)
    print(eye_pairs)
    remove = []
    for (sx, sy, sw, sh) in smiles:
        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 255, 20), 2)
        if sy + (sh / 2) < (h / 2):
            remove.append(False)
        else:
            if sx + (sw/2) > center_min and sx + (sw/2) < center_max:
                remove.append(True)
            else:
                remove.append(False)
    smiles = list(it.compress(smiles, remove))
    if len(smiles) is 1:
        Smile = True
    else:
        save_json(Face, Eyes, Smile)

cv2.imwrite('Detected.jpg', resized_img)
save_json(Face, Eyes, Smile)

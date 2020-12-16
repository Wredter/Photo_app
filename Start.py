from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import cv2
# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=800, margin=0)

img = cv2.imread("\\Data\\CV_photo.jpg", cv2.IMREAD_UNCHANGED)

print("Size : ", img.shape)
scale_percen = 40

# import the necessary packages
# from pyimagesearch import imutils
import numpy as np
import argparse
import matplotlib
from matplotlib import pyplot as plt

import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower1 = np.array([0, 0, 0], dtype="uint8")
upper1 = np.array([30, 255, 255], dtype="uint8")

lower2 = np.array([150, 0, 0], dtype="uint8")
upper2 = np.array([180, 255, 255], dtype="uint8")

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping over the frames in the video
# grab the current frame

frame = cv2.imread('i3.png')
# (grabbed, frame) = camera.read()
# if we are viewing a video and we did not grab a
# frame, then we have reached the end of the video
# if args.get("video") and not grabbed:
# break

    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    # frame = imutils.resize(frame, width=400)
rows, cols, _ =frame.shape
# frame = draw_rect(frame)
converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
cv2.imshow('test',frame);
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
h = hsv[:,:,0]
hist = cv2.calcHist([h], [0], None, [180], [0, 180])
plt.plot(hist)

h = hsv[:,:,1]
hist = cv2.calcHist([h], [0], None, [255], [0, 255])
plt.plot(hist)

h = hsv[:,:,2]
hist = cv2.calcHist([h], [0], None, [255], [0, 255])
plt.plot(hist)
plt.show()


# hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
# plt.imshow(hist)

# plt.hist(frame.ravel(), 256, [0, 256]);

# cv2.imshow('test',converted)
skinMask = cv2.inRange(converted, lower1, upper1)
skinMask = cv2.inRange(converted, lower2, upper2)

# apply a series of erosions and dilations to the mask
# using an elliptical kernel
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

mask1 = cv2.erode(skinMask, kernel, iterations=2)
mask2 = cv2.dilate(skinMask, kernel, iterations=2)
skinMask = np.bitwise_and(mask1, mask2)

# blur the mask to help remove noise, then apply the
# mask to the frame
skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
skin = cv2.bitwise_and(frame, frame, mask=skinMask)

# show the skin in the image along with the mask
# cv2.imshow("images", np.hstack([frame, skin]))
# if the 'q' key is pressed, stop the loop
while True:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
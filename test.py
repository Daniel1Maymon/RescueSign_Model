import sys
import cv2
import flask
import flask_cors

print(sys.path)

img = cv2.imread("play.png", cv2.IMREAD_COLOR)

print("img = ")
print(img)
# cv2.imshow("image", img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
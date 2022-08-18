import cv2
import numpy as np
import urllib.request

# url_path = "http://s0.geograph.org.uk/photos/40/57/405725_b17937da.jpg"
url_path = "https://i.pinimg.com/originals/f5/a8/28/f5a828b4f3ddd3b3444bcd7d856ccb6a.jpg"

with urllib.request.urlopen(url_path) as url:
    url_response = url.read()
    print("Opening URL image from path :", url_path)

img_array = np.array(bytearray(url_response), dtype=np.uint8)

img = cv2.imdecode(img_array, -1)

cv2.imshow('URL Image', img)
cv2.waitKey()

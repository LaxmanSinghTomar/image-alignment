# Flask App for Image Alignment

# Import Libraries and Packages
from flask import Flask, request, jsonify
from PIL import Image
import utils
import numpy as np
import cv2
import os, errno

app = Flask(__name__)

# Create Directory for Corrected Images
import os
try:
    os.makedirs('corrected_images')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

def correct(img):
    """
    Return Image with Corrected Alignment.

    Note: 
        Input must be an Numpy Array Image.

    Args:
        img(np.array) : Numpy Array Image.

    Returns:
        Image with Correct Alignment.
    """
    # Convert the Image to GrayScale and Flip F/G and B/G such that F/G="white" & B/G="black"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # Threshold Image, setting F/G pixels=255 & B/G pixels=0
    thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Grab coordinates of all pixels > 0, then use these to calculate rotated bounding box which contains all coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        # adding 90 degress to angle if rectangle rotates clockwise
        angle = -(90 + angle)
    else:
        # otherwise, just opposite of angle to make it positive.
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

@app.route('/')
def index():
    return """ Server works! <hr>
    <form action = "/correct" method = "POST" enctype="multipart/form-data">
    <input type = "file" name="image">
    <button>OK<button> 
    </form>
    """

@app.route("/correct", methods=['POST'])
def fix():
    file = request.files['image']
    img = Image.open(file.stream)

    np_img = np.array(img)
    corrected_img = correct(np_img)

    data = utils.image_to_base64(corrected_img).decode()
    
    utils.base64_to_image(data, "corrected_images/correct.jpg")
    
    return jsonify({
        "msg": "success",
        "size": [img.width, img.height],
        "format": img.format,
        "img" : data
    })
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

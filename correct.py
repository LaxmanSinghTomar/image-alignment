# Correct Alignment of Images

# Import Libraries and Packages
import numpy as np
import cv2
import os, errno
import argparse

# Create Directory for Corrected Images
import os
try:
    os.makedirs('corrected_images')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


def correct(img_path):
    """
    Return Image with Corrected Alignment.

    Note: 
        Input must be Image Path.

    Args:
        img_path(Path) : Image Path.

    Returns:
        Image with Correct Alignment.
    """
    # Load Image
    image = cv2.imread(img_path)

    # Convert the Image to GrayScale and Flip F/G and B/G such that F/G="white" & B/G="black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

    # Rotate Image to Correct Alignment
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def correct_images(dir_path):
    """
    Correct Images in a given Directory.

    Note:
        Input must be a directory path.

    Args:
        dir_path(Path) : Directory Path.

    Returns:
        None
    """
    try:
        for file in os.listdir(dir_path):
            corrected = correct(f"{dir_path}{file}")
            cv2.imwrite(f"corrected_images/corrected_{file}", corrected)
            print(f"{file} parsed!")
    except Exception as e:
        print(e)

if __name__== "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need directory path of images
    parser.add_argument("--dir_path", type=str)

    # read the arguments from the command line
    args = parser.parse_args()

    # run the correct_images specified by command line arguments
    correct_images(dir_path=args.dir_path)


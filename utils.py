# Utilities Functions

# Importing Libraries and Packages
import base64
from PIL import Image
from io import BytesIO
import cv2

def image_to_base64(img):
    """
    Converts Image to Base64 Encoded Image.

    Note:
        Input must be a Numpy Array Image.

    Arguments:
        img(np.ndarray) : Image.

    Returns:
        Base64 Encoded Image.
    """
    _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    data = base64.b64encode(im_bytes)
    return data

def base64_to_image(data, file_path):
    """
    Converts Base64 Encoded Image to Image and saves in given path.

    Note:
        data must be a Base 64 Encoded Image.
    
    Args:
        data(bytes) : Base64 Encoded Image.
        file_path(Path) : File Path.

    Returns:
        None
    """
    img = Image.open(BytesIO(base64.b64decode(data)))
    img.save(file_path, 'PNG')
    print(f"Image Saved at {file_path}")

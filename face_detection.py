from io import BytesIO
import base64
import dlib
import cv2
import requests
import numpy as np

def detect_faces(image_url, is_face):
    """
    Function to convert image source url to base64 image with
    face detected on it or without, depending on second argument

    Args:
        image_url: image source url.
        is_face: bolean, whether to find face or no.

    Returns:
        Returns base64 image string.
    """
    response = requests.get(image_url, timeout=10)
    image_bytes = BytesIO(response.content)

    arr = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(arr, -1)

    if is_face:
        # Load the pre-trained face detector model from dlib
        detector = dlib.get_frontal_face_detector()
        # Convert the image to grayscale (dlib works on grayscale images)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            # Draw rectangle around the face
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Convert the image to JPEG format
    _, encoded_image = cv2.imencode('.jpg', image)

    # Encode the image as base64
    base64_image = base64.b64encode(encoded_image).decode('utf-8')

    return f"data:image/jpeg;base64,{base64_image}"

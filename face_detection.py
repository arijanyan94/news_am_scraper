import dlib
import cv2
import base64
import requests
import numpy as np
from io import BytesIO

def detect_faces(image_url, is_face):

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    # Decode the image using OpenCV
    arr = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(arr, -1)

    if is_face:
        # Load the pre-trained face detector model from dlib
        detector = dlib.get_frontal_face_detector()

        # Convert the image to grayscale (dlib works on grayscale images)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = detector(gray, 1)

        # Loop through each face and draw a rectangle around it
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around the face

    # Convert the image to JPEG format
    _, encoded_image = cv2.imencode('.jpg', image)
    
    # Encode the image as base64
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_image}"
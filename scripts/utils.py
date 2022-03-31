import cv2
import base64
from io import BytesIO
from PIL import Image
import numpy as np

def reduce_size(frame, scale_percent=80):
    # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    return resized

def make_square(frame):
    h,w = frame.shape[:2]
    future_dimension = min(h,w)
    squared_frame = frame[:future_dimension,:future_dimension,:3]
    
    return squared_frame

def make_arrays(base64_images_array):
    frames = [str_decode_img(img_b64) for img_b64 in base64_images_array]
    
    return frames
    
def save_image(path,frame):
    cv2.imwrite(path,frame)

def str_enconde_img_mat(frame):
    _, buffer = cv2.imencode('.jpg',frame)
    img_b64 = base64.b64encode(buffer)
    img_str = img_b64.decode('utf-8')
    
    return img_str 

def str_encode_img_file(image_path):
    frame = cv2.imread(image_path)
    _, buffer = cv2.imencode('.jpg',frame)
    
    img_b64 = base64.b64encode(buffer)
    img_str = img_b64.decode('utf-8')

    return img_str 

def str_encode_img_web(image_content):
    img_b64 = base64.b64encode(image_content)
    img_str = img_b64.decode('utf-8')

    return img_str 

def str_decode_img(image_b64):
    img = base64.b64decode(image_b64)
    img = BytesIO(img) 
    img = Image.open(img)
    img = np.array(img)
    
    return img

def str_decode_to_BytesIO(image_b64):
    img = base64.b64decode(image_b64)
    img = BytesIO(img) 
    
    return img

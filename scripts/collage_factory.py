import numpy as np
from utils import make_square,reduce_size

def make_1x1_image(frame):
    
    normalized_frame = make_square(frame)
    return normalized_frame

def make_2x2_image(frames):
    
    normalized_frames= [make_1x1_image(frame) for frame in frames]
    img1 = normalized_frames[0]
    img2 = normalized_frames[1]
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    #create empty martrix (Mat)
    black_board = np.zeros(shape=(h1+ h2, w1 + w2, 3), dtype=np.uint8)
    
    #placing img1
    black_board[:h1, :w1,:3]=img1
    #placing img2
    black_board[h1:h1+h2, w1:w1+w2,:3]=img2

    return black_board

def make_3x3_image(frames,single):
    collage_2x2 = make_2x2_image(frames)
    h1, w1 = collage_2x2.shape[:2]


    single_image= reduce_size(make_1x1_image(single))
    h2, w2 = single_image.shape[:2]

    centered_col= (int(h1/2) -int(h2/2))
    centered_row= (int(w1/2) -int(w2/2))


    collage_2x2[centered_col:centered_col+h2,centered_row:centered_row+w2,:3]=single_image

    return collage_2x2

def rec_nxn_base(images:list):
    if len(images)==1:
        return make_1x1_image(images[0])
    return rec_nxn(images)

def rec_nxn(images:list):
    size = len(images)

    if size==2:
        return make_2x2_image(images)
    if size==3:
        return make_3x3_image(images[:2],make_1x1_image(images[-1]))
    
    if size%2==0:
        return make_2x2_image([rec_nxn(images[:size//2]) , rec_nxn(images[size//2:])])
    else:
        return make_3x3_image([rec_nxn(images[:size//2]) , rec_nxn(images[size//2:-1])], make_1x1_image(images[-1]))


import numpy as np
import requests
from pyunsplash import PyUnsplash
from common import load_configuration_item, load_from_cache
from utils import str_encode_img_file,str_encode_img_web

"""
should return b64 encoding of the picture
"""

def download_from_unsplash(amount, query):
    if (amount==0):
        return []

    UNSPLASH_ACCESS_KEY = load_configuration_item("access_key")

    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)

    photos = pu.photos(type_='random', count=amount, featured=True, query= query)

    photo_entries = photos.entries

    str_images= []
    for photo in photo_entries:
        #print(photo.id, photo.link_download)
        image_path=f'./tmp_downloads/splashed_{photo.id}.jpg'
        response = requests.get(photo.link_download, allow_redirects=True)
        
        #saving the image so I dont need to request over and over again from unsplash
        open(image_path, 'wb').write(response.content)
        
      
        #but I am originally interested in the str representation of the image
        img_str= str_encode_img_web(response.content)

        str_images.append(img_str)
    
    return str_images
    
"""
should return b64 encoding of the picture
"""
def download_unsplash_images(site,amount=3,query='architecture'):

    path_cached_images= []
    amount_catched= len(path_cached_images)

    if amount_catched > 0:
        
        str_enc_cached_images = [str_encode_img_file(path) for path in path_cached_images]
        
        if(amount_catched>=amount):
            return str_enc_cached_images[:amount]
        else:    
            amount_needed_to_fech = amount-amount_catched    
            unsplash_str_enc_images = download_from_unsplash(amount_needed_to_fech, query)

            return str_enc_cached_images + unsplash_str_enc_images
    else:
        return download_from_unsplash(amount, query)


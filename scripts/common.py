import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

def load_configuration_item(key_to_fetch):
    config_path = join(dirname(abspath("__file__")), 'env/.config')

    load_dotenv(config_path)
    value = os.environ.get(key_to_fetch)
    
    return value

def load_from_cache(prefix_folder ='tmp_downloads'):
    
    downloads_path = join(dirname(abspath("__file__")), prefix_folder)
   
    path_images = [join( downloads_path, image_name) for image_name in os.listdir(downloads_path)]
    return path_images


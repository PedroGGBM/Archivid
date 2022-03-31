from collage_factory import rec_nxn_base
from utils import make_arrays,save_image, str_enconde_img_mat

from api_dal import download_unsplash_images

class Collage_Maker:

    def __init__(self):
        self.factory = {
            'unsplash':download_unsplash_images,
            'encoding_array':None
        }

    def create_collage(self, amount_of_images=3, query='architecture', source ='encoding_array', site_or_table = None, encodings_b64=[]):
        
        concrete_maker = self.factory[source]
 
        if source == 'unsplash':
            b64_images_array = concrete_maker(site_or_table, amount_of_images, query)
        else:
            b64_images_array = encodings_b64[:amount_of_images]

        images_as_cv2arrays = make_arrays(b64_images_array)
        collage = rec_nxn_base(images_as_cv2arrays)

        return str_enconde_img_mat(collage)
    

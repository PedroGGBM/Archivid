from sql_dal import SQL_DAL
import uuid
from hasher_functionalities import hash_password

class studio_gronda_proj_CRUD(SQL_DAL):
    
    def __init__(self):
        super().__init__()
        self.entity_name = "studio_gronda_proj"
    
    def insert_image(self,record_dict):
        id = str(uuid.uuid4())
        property_type = record_dict['property_type']
        location = record_dict['location']
        image_str = record_dict['image_str']

        image_existing = super().load_record_by_id(self.entity_name,id)

        if not image_existing:
        
            super().insert_record(self.entity_name,(id,property_type,location,image_str))
            return True
        else:
            return False

    def load_image_by_id(self,id):
        
        image_existing = super().load_record_by_id(self.entity_name,id)
        return True if image_existing else False
    
    def load_all_images(self):
        return super().load_table_records(self.entity_name)
    
    def remove_image(self, id):
        return super().remove_record(self.entity_name, id)



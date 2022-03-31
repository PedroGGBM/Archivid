from sql_dal import SQL_DAL
import uuid
from hasher_functionalities import hash_password

class User_CRUD(SQL_DAL):
    
    def __init__(self):
        super().__init__()
        self.entity_name = "users"
    
    def insert_user(self, record_dict):
        id = record_dict['id'] if 'id' in record_dict.keys()!=None else str(uuid.uuid4())
        user_name = record_dict['user_name']
        plane_pwd = record_dict['password']
        email = record_dict['email']

        user_existing = super().load_record_by_column(table_name=self.entity_name,column_id=2,column_value=email)

        if not user_existing:
            hashed_pass,salt_used = hash_password(plane_pwd)
            super().insert_record(self.entity_name,(id,user_name,email,hashed_pass,salt_used))
            return True
        else:
            return False

    def load_user_by_id(self,id):
        
        user_existing = super().load_record_by_id(self.entity_name,id)
        return True if user_existing else False
    
    def load_all_users(self): # not in use --> extension 
        return super().load_table_records(self.entity_name)
    
    def remove_user(self, id): # not in use --> extension 
        return super().remove_record(self.entity_name, id)
    
    def login(self, record_dict):
        
        user_name = record_dict['user_name']
        plane_pwd = record_dict['password']
        email = record_dict['email']

        user_existing = super().load_record_by_column(self.entity_name, column_value= email, column_id= 2)

        if not user_existing:
            return False
        else:
            pass_in_db = user_existing[3]
            salt_in_db = user_existing[4]
            user_name_in_db = user_existing[1]

            hashed_pass,_ = hash_password(plane_pwd,salt_in_db)
            if hashed_pass == pass_in_db and user_name == user_name_in_db:
                return True
            return False

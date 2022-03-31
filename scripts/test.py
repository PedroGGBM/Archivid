from ctypes import util
from email import utils
from unicodedata import category
import uuid
import random

import cv2

from numpy import record
from common import load_from_cache
from studio_proj_crud import studio_gronda_proj_CRUD
from user_crud import User_CRUD
from sql_dal import SQL_DAL
from collage_maker import Collage_Maker
from utils import make_arrays, str_encode_img_file

def sql_load_table_test():
    sql_dal_obj= SQL_DAL()

    records= sql_dal_obj.load_table_records("users")
    for item in records:
        print(item)

def sql_load_table_test():
    sql_dal_obj= SQL_DAL()

    records= sql_dal_obj.load_table_records("users")
    for item in records:
        print(item)

def sql_insertion_many_test():

    a =("234234","machucha","dveliz900@gmail.com","dummy_pasword",)
    b =("342342","ivan","dveliz900@gmail.com","dummy_pasword",)
    sql_dal_obj= SQL_DAL()

    sql_dal_obj.insert_many_records("users",[a,b])

    records= sql_dal_obj.load_table_records("users")
    for item in records:
        print(item)
   
def sql_insertion_one_test():

    c =("284234","marina","dveliz900@gmail.com","dummy_pasword",)
    
    sql_dal_obj= SQL_DAL()

    sql_dal_obj.insert_record("users",c)

    records= sql_dal_obj.load_table_records("users")
    for item in records:
        print(item)

def sql_remove_test():
    sql_dal_obj= SQL_DAL()
    sql_dal_obj.remove_record("users","234234")

def sql_insert_image_test():
    cached_files = load_from_cache(prefix_folder="test_pictures/cat_hotel/")
    str_enc_cached_images = [str_encode_img_file(path) for path in cached_files]
    
    a =("1000","hotel","andalucia",str_enc_cached_images[0])
    b =("1001","hotel","barcelona",str_enc_cached_images[1])
    c =("1002","hotel","somwhere",str_enc_cached_images[2])
    
    sql_dal_obj= SQL_DAL()

    sql_dal_obj.insert_record("studio_gronda",c)

def sql_insert_many_images_test():
    cached_files = load_from_cache(prefix_folder="test_pictures/cat_building/")
    str_enc_cached_images = [str_encode_img_file(path) for path in cached_files]
    
    a =("1004","building","malaga",str_enc_cached_images[0])
    b =("1005","building","portugal",str_enc_cached_images[1])
    
    
    sql_dal_obj= SQL_DAL()

    sql_dal_obj.insert_many_records("studio_gronda",[a,b])

def scrapper_test():
    collage_obj = Collage_Maker()

    str_image = collage_obj.create_collage(3,source="webscrapper")    

from studio_talent_crud import studio_talent_CRUD

def unsplash_test():
    collage_obj = Collage_Maker()

    str_image=collage_obj.create_collage(2,source="unsplash")

    studio_tlt_CRUD = studio_talent_CRUD()

    record={
            'id':None,
            'property_type':'none',
            'location':'none',
            'image_str':str_image
        }
    was_inserted = studio_tlt_CRUD.insert_image(record)   

def sql_collage_test():
    collage_obj = Collage_Maker()

    str_image=collage_obj.create_collage(2,source="sql_images",site_or_table="studio_gronda.building")   

def sql_collage_any_cat_test():
    collage_obj = Collage_Maker()

    str_image = collage_obj.create_collage(5,source="sql_images",site_or_table="studio_gronda")  

def test_userCRUD_insert():
    user_crud = User_CRUD()
    record ={
        "user_name":"Andrea",
        "password":"holaAndrea",
        "email":"andrea@gmail.com"
    }
    was_inserted= user_crud.insert_user(record)
    print(was_inserted)

def test_userCRUD_load():
    user_crud = User_CRUD()
    record ={
        "id":"5b549669-4517-4390-8cb8-a2543c219a73",
        "user_name":"Andrea",
        "password":"holaAndrea",
        "email":"andrea@gmail.com"
    }
    users= user_crud.load_all_users()
    if users:
        for user in users:
            print(user)
    else:
        print("nothing found")

def test_userCRUD_load_id():
    user_crud = User_CRUD()
    record ={
        "id":"5b549669-4517-4390-8cb8-a2543c219a73",
        "user_name":"Andrea",
        "password":"holaAndrea",
        "email":"andrea@gmail.com"
    }
    users_found= user_crud.load_user_by_id(record['id'])
    print(users_found)

def test_userCRUD_login_success():
    user_crud = User_CRUD()
    record ={
        "id":"861863f7-7d15-457a-ac0e-a879eef7b438",
        "user_name":"Andrea",
        "password":"holaAndrea",
        "email":"andrea@gmail.com"
    }
    can_log= user_crud.login(record)
    print(can_log)

def sql_insert_many_images_test_for_categories(category_name):
    cached_files = load_from_cache(prefix_folder=f"scripts/test_pictures/cat_{category_name}/")
    str_enc_cached_images = [str_encode_img_file(path) for path in cached_files]
    
    records_ready =[]

    for encoding in str_enc_cached_images:
        a =(str(uuid.uuid4()),category_name,"none",encoding)
        records_ready.append(a)
    
    sql_dal_obj= SQL_DAL()

    sql_dal_obj.insert_many_records("studio_gronda_proj",records_ready)

def inserter_many():
    categories=[
            'All_Projects',
            'Architecture',
            'Hotel',
            'Restaurant_Bar',
            'Spa_Wellness',
            'Entertainment',
            'Residential',
            'Masterplan'
            ]
    #test_userCRUD_insert()
    for cat in categories:
        try:
            sql_insert_many_images_test_for_categories(cat)
            print(f"Category {cat} completed")
        except:
            print(f"problem in cat : {cat}, probably doesnt exist in folder")
    print("call any test function here")

def filter_by_ones():
    cat_values = [0,0,1,1,1,1,0,1]

    collage_obj = Collage_Maker()
    studio_prj_CRUD= studio_gronda_proj_CRUD()

    cat_strings=[
            'All_Projects',
            'Architecture',
            'Hotel',
            'Restaurant_Bar',
            'Spa_Wellness',
            'Entertainment',
            'Residential',
            'Masterplan'
            ]
    records=  studio_prj_CRUD.load_all_images()

    string_activated= [cat_strings[i] for i,item in enumerate(cat_values) if item==1]

    #1 represents the property type
    filterd_img_results = [photo_record[3] for photo_record in records if photo_record[1] in string_activated]

    random.shuffle(filterd_img_results)

    for i in range(1):
        str_image=collage_obj.create_collage(amount_of_images= 3,encodings_b64=filterd_img_results)
        random.shuffle(filterd_img_results)

        
        record={
            'id':None,
            'property_type':'collage',
            'location':'none',
            'image_str':str_image
        }
        was_inserted = studio_prj_CRUD.insert_image(record)
        if was_inserted:
            print(f"collage {i}-th properly save in db")
        else:
            print("nop")
    print("done")


def test_scrapper_archiv():
    
    b64strings_img= scrap_site(amount_of_images=10,query="masterplan")
    if b64strings_img:
        print("cool",len(b64strings_img))

        #frames= make_arrays(base64_images_array=b64strings_img)
        #cv2.imshow("got",frames[0])
        #cv2.waitKey(0)
        

    else:
        print("bss")


def main():
    inserter_many()
    print("done")

main()
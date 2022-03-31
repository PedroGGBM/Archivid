
# essential
from cgitb import text
import tkinter as tk
import numpy as np
import tkinter.font as font
import os, sys
import cv2
import random

# image
from PIL import Image, ImageTk
from collage_maker import Collage_Maker
from archivid_scrapper import parse_and_save
from utils import str_decode_to_BytesIO

# # CRUDs import
from studio_proj_crud import studio_gronda_proj_CRUD
from studio_client_crud import studio_client_CRUD
from studio_talent_crud import studio_talent_CRUD
# # user CRUD for login/register
from user_crud import User_CRUD 

# collage maker
collage_obj = Collage_Maker()

# CRUDs
user_crud = User_CRUD()
studio_tlt_CRUD = studio_talent_CRUD()
studio_prj_CRUD= studio_gronda_proj_CRUD()
studio_clt_CRUD = studio_client_CRUD()

def crud_factory():
    dictn = {
        "talent": studio_tlt_CRUD,
        "proj": studio_prj_CRUD,
        "client": studio_clt_CRUD
    }

    return dictn

def filter_factory():
    dict_filter={
        "talent": lambda x: x[1]=='none',
        "proj": lambda x: x[1]=='collage',
        "client": lambda x: x[1]=='collages.client'
    }
    return dict_filter

def register_success():
    global screen_3

    screen_3 = tk.Toplevel(root)
    screen_3.title('Success')
    screen_3.geometry('300x100')
    tk.Label(screen_3, text= 'Register success').pack()
    tk.Button(screen_3, text= 'Continue', command= lambda:[screen_1.destroy(), screen_3.destroy()]).pack()

def email_already_used():
    global screen_4

    screen_4 = tk.Toplevel(root)
    screen_4.title('Register Error')
    screen_4.geometry('300x100')
    tk.Label(screen_4, text= 'Email already in use (user exists)').pack()
    tk.Button(screen_4, text= 'Continue', command= screen_4.destroy).pack()

def login_success():
    global screen_5

    screen_5 = tk.Toplevel(root)
    screen_5.title('Login Success')
    screen_5.geometry('300x100')
    tk.Label(screen_5, text= 'Login success').pack()
    tk.Button(screen_5, text= 'Continue', command= lambda:[screen_2.destroy(), screen_5.destroy(), 
                                                           loginframe.destroy(), mainview(root)]).pack()

def user_not_found():
    global screen_6

    screen_6 = tk.Toplevel(root)
    screen_6.title('Login Error')
    screen_6.geometry('300x100')
    tk.Label(screen_6, text= 'Incorrect username/password').pack()
    tk.Button(screen_6, text= 'Continue', command= lambda: screen_6.destroy()).pack()

def register_user(email, username, password, email_entry, username_entry, password_entry):
    email_info = email.get()
    username_info = username.get()
    password_info = password.get()

    email_entry.delete(0, 'end')
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

    record ={
        "user_name":username_info,
        "password":password_info,
        "email":email_info
    }
    
    was_inserted = user_crud.insert_user(record) # return True or False if email (user) already registered

    if was_inserted:
        register_success()
    else:
        email_already_used()

def login_user(email, username, password, email_entry, username_entry, password_entry):
    email_info = email.get()
    username_info = username.get()
    password_info = password.get()

    email_entry.delete(0, 'end')
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

    record = {
        "user_name":username_info,
        "password":password_info,
        "email":email_info
    }

    can_log = user_crud.login(record)

    if can_log:
        login_success() 
    else:
        user_not_found()

def register():
    global screen_1
    
    screen_1 = tk.Toplevel(root)
    screen_1.title('Register')

    screen_1.geometry('300x300')

    email = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(screen_1, text= 'Enter details below').pack()
    tk.Label(screen_1, text= '').pack()

    # email entry
    tk.Label(screen_1, text= 'Email').pack()
    email_entry = tk.Entry(screen_1, textvariable= email)
    email_entry.pack()

    # username entry 
    tk.Label(screen_1, text= 'Username').pack()
    username_entry = tk.Entry(screen_1, textvariable= username)
    username_entry.pack()

    # password entry 
    tk.Label(screen_1, text= 'Password').pack() 
    password_entry = tk.Entry(screen_1, show= '*', textvariable= password)
    password_entry.pack()

    tk.Label(screen_1, text= '').pack()
    tk.Button(screen_1, text= 'Register', width= 10, height= 1, command= lambda: register_user(email, username, password,
                                                                                 email_entry, username_entry, password_entry)).pack()   
                                                                            
def login():
    global screen_2

    screen_2 = tk.Toplevel(root)
    screen_2.title('Login')
    screen_2.geometry('300x300')

    tk.Label(screen_2, text= 'Enter details below').pack()
    tk.Label(screen_2, text= '').pack()

    email = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(screen_2, text= 'Email').pack()
    email_entry = tk.Entry(screen_2, textvariable = email)
    email_entry.pack()

    tk.Label(screen_2, text= 'Username').pack()
    username_entry = tk.Entry(screen_2, textvariable = username)
    username_entry.pack()
    
    tk.Label(screen_2, text= 'Password').pack()
    password_entry = tk.Entry(screen_2, show= '*', textvariable = password)
    password_entry.pack()

    tk.Label(screen_2, text= '').pack()
    tk.Button(screen_2, text= 'Login', width= 10, height= 1, command= lambda: login_user(email, username, password, 
                                                                              email_entry, username_entry, password_entry)).pack()

""" CREATE COLLAGE AND VISUALIZE """

def load_imagetk_photoimages(crud):
    
    Image.MAX_IMAGE_PIXELS = None # set maximum pixel density to None (no limit)

    image_lst_tk = []
    image_lst_nparr = []
    image_records = crud_factory()[crud].load_all_images()
    image_records = filter(filter_factory()[crud],image_records)

    for photo_info in image_records:
        photo = photo_info[3]
        
        photo = str_decode_to_BytesIO(photo)
        image_lst_tk.append(ImageTk.PhotoImage(Image.open(photo).resize((600, 600))))
        image_lst_nparr.append(np.array(Image.open(photo).resize((1000, 1000))))

    return image_lst_tk, image_lst_nparr

def delete_img(index_img, img_lst, crud):

    if len(img_lst)==0: # if there are no images to display
        return 

    image_records = crud_factory()[crud].load_all_images() # grabs all images in the proj table
    image_records = list(filter(filter_factory()[crud],image_records)) # filters all the collages in the proj table
    img_id = image_records[index_img[0]] # gets the id of the deleted collage 

    crud_factory()[crud].remove_image(img_id[0])
    img_lst.clear() # clears list

    img, _ = load_imagetk_photoimages(crud) # fetches images from corresponding table and converts them to imagetk imgs
    img_lst.extend(img) # loads the images once again

def display(index_img, img_lst_nparr):
    window_name = 'Display Collage'
    # print(index_img[0])
    img = img_lst_nparr[index_img[0]]

    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def update_number_forward(number_lst, image_label_cont, img_lst, img_status):
    
    if len(img_lst)==0: # if there are no images to display
        return 

    number_lst[0] += 1 # passing by reference 
    number_lst[0] = number_lst[0] % len(img_lst)
    current_num = number_lst[0]

    image_label_cont.config(image= img_lst[current_num])
    img_status.config(text= f'Image {current_num+1} of {len(img_lst)}')

def update_number_back(number_lst, image_label_cont, img_lst, img_status):
    
    if len(img_lst)==0: # if there are no images to display
        return 
    
    number_lst[0] -= 1 # passing by reference
    number_lst[0] = number_lst[0] % len(img_lst)
    current_num = number_lst[0]

    image_label_cont.config(image= img_lst[current_num])
    img_status.config(text= f'Image {current_num+1} of {len(img_lst)}')

def visualize(frame, crud_select):
    global vis_fm

    vis_fm = tk.LabelFrame(frame, text= ' Visualize Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    vis_fm.pack(fill= 'both', expand= True, padx= 0, pady= 0)

    # list of ImageTk images and np.array images
    img_lst, img_lst_nparr = load_imagetk_photoimages(crud_select)
    
    # current index
    index_img = [0]
    # init img
    try:
        my_label = tk.Label(vis_fm, image= img_lst[index_img[0]])
        my_label.pack(padx= 1, pady= 5)
    except IndexError:
        print('No images found in database')

    # image counter status
    img_status = tk.Label(vis_fm, text= f'Image 1 of {len(img_lst)}', bd = 1, relief= 'sunken')
    img_status.place(relx= 0.5, rely= 0.95, anchor= 'c')

    button_backward = tk.Button(vis_fm, text= '<<', height = '1', width = '2', command= lambda: update_number_back(index_img, my_label, img_lst, img_status))
    button_delete = tk.Button(vis_fm, text= 'DELETE COLLAGE', height = '1', width = '14', command= lambda: delete_img(index_img, img_lst, crud_select))
    button_display = tk.Button(vis_fm, text= 'DISPLAY', height = '1', width = '14', command= lambda: display(index_img, img_lst_nparr))
    button_forward = tk.Button(vis_fm, text= '>>', height = '1', width = '2', command= lambda: update_number_forward(index_img, my_label, img_lst, img_status))

    button_backward.place(relx= 0.1, rely= 0.9, anchor= 'w')
    button_delete.place(relx= 0.4, rely= 0.9, anchor= 'c')
    button_display.place(relx= 0.6, rely= 0.9, anchor= 'c')
    button_forward.place(relx= 0.9, rely= 0.9, anchor= 'e')

    back_bt = tk.Button(vis_fm, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= vis_fm.destroy)
    back_bt.place(relx= 0.04, rely= 0.04, anchor= 'nw')

""" [] Generate Talent Collages [] """

def gen_talent_coll(imgxcoll_, numofcoll_, query):
    images_per_collage = imgxcoll_.get()
    times_2b_called = numofcoll_.get()
    unsplash_query = query.get()

    for i in range(times_2b_called):
        str_image = collage_obj.create_collage(images_per_collage, query= str(unsplash_query), source="unsplash")
        
        record = {
            'id':None,
            'property_type':'none',
            'location':'none',
            'image_str':str_image
        }

        was_inserted = studio_tlt_CRUD.insert_image(record)
        if was_inserted:
            print(f"collage {i}-th properly save in db")
        else:
            print("Error: collage no properly saved in db")
    print("done")

def talent_coll():
    talent = tk.LabelFrame(talent_fm, text= ' Add Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    talent.pack(fill= 'both', expand= True, padx= 0, pady= 0)

    imgxcoll_ = tk.IntVar(value= 1)
    numofcoll_ = tk.IntVar(value= 1)
    query = tk.StringVar()
    styleofcoll1_ = tk.IntVar()
    styleofcoll2_ = tk.IntVar()

    tk.Label(talent, text = 'Images per collage: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.1, rely= 0.2, anchor= 'w')
    imgxcoll = tk.Entry(talent, textvariable = imgxcoll_, font= ('Josefin Slab', 14, 'bold'))
    imgxcoll.place(relx= 0.1, rely= 0.25, anchor= 'w')

    tk.Label(talent, text = 'Number of collages: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.1, rely= 0.4, anchor= 'w')
    numofcoll = tk.Entry(talent, textvariable = numofcoll_, font= ('Josefin Slab', 14, 'bold'))
    numofcoll.place(relx= 0.1, rely= 0.45, anchor= 'w')

    tk.Label(talent, text = 'Query: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.1, rely= 0.6, anchor= 'w')
    numofcoll = tk.Entry(talent, textvariable = query, font= ('Josefin Slab', 14, 'bold'))
    numofcoll.place(relx= 0.1, rely= 0.65, anchor= 'w')

    back_bt = tk.Button(talent, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= talent.destroy)
    back_bt.place(relx= 0.04, rely= 0.04, anchor= 'nw')

    generate = tk.Button(talent, text = 'Generate', font= ('Josefin Slab', 14, 'bold'), command= lambda:gen_talent_coll(imgxcoll_, numofcoll_, query))
    generate.place(relx= 0.1, rely= 0.75, anchor= 'w')

""" [] Generate Project Collages [] """

def gen_proj_coll(check_box_ctrls,imgxcoll_,numofcoll_):

    cat_values =[item.get() for item in check_box_ctrls]
    
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
    
    records = studio_prj_CRUD.load_all_images()

    string_activated = [cat_strings[i] for i, item in enumerate(cat_values) if item==1]
    # print(string_activated, cat_values, len(string_activated))
    
    # 1 represents the property type
    filtered_img_results = [photo_record[3] for photo_record in records if photo_record[1] in string_activated]
    if (len(filtered_img_results)==0):
        print("No Image Category Selected")
        return

    random.shuffle(filtered_img_results)

    for i in range(numofcoll_.get()):
        str_image = collage_obj.create_collage(amount_of_images= imgxcoll_.get(),encodings_b64= filtered_img_results)
        random.shuffle(filtered_img_results)

        record = {
            'id':None,
            'property_type':'collage',
            'location':'none',
            'image_str':str_image
        }

        was_inserted = studio_prj_CRUD.insert_image(record)
        
        if was_inserted:
            print(f"collage {i}-th properly save in db")
        else:
            print("Error: collage not saved in db")
    print("done")

def proj_coll():
    proj = tk.LabelFrame(proj_fm, text= ' Add Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    proj.pack(fill= 'both', expand= True, padx= 0, pady= 0)

    mult_selec_font = ('Josefin Slab', 12, 'bold')

    lb = tk.Label(proj, text= ' Select type of StudioGRONDA project: ', font= mult_selec_font)
    lb.place(relx= 0.1, rely= 0.13, anchor= 'w')

    c1_ = tk.IntVar() # 1 if checkboxed, 0 if not
    c2_ = tk.IntVar()
    c3_ = tk.IntVar()
    c4_ = tk.IntVar()
    c5_ = tk.IntVar()
    c6_ = tk.IntVar()
    c7_ = tk.IntVar()
    c8_ = tk.IntVar()

    c1 = tk.Checkbutton(proj, text= 'All Projects', variable= c1_, font= mult_selec_font)
    c2 = tk.Checkbutton(proj, text= 'Architecture', variable= c2_, font= mult_selec_font)
    c3 = tk.Checkbutton(proj, text= 'Hotel', variable= c3_, font= mult_selec_font)
    c4 = tk.Checkbutton(proj, text= 'Restaurant/Bar', variable= c4_, font= mult_selec_font)
    c5 = tk.Checkbutton(proj, text= 'Spa/Wellness', variable= c5_, font= mult_selec_font)
    c6 = tk.Checkbutton(proj, text= 'Entertainment', variable= c6_, font= mult_selec_font)
    c7 = tk.Checkbutton(proj, text= 'Residential', variable= c7_, font= mult_selec_font)
    c8 = tk.Checkbutton(proj, text= 'Masterplan', variable= c8_, font= mult_selec_font)

    c1.place(relx= 0.1, rely= 0.2, anchor= 'w')
    c2.place(relx= 0.1, rely= 0.27, anchor= 'w')
    c3.place(relx= 0.1, rely= 0.34, anchor= 'w')
    c4.place(relx= 0.1, rely= 0.41, anchor= 'w')
    c5.place(relx= 0.1, rely= 0.48, anchor= 'w')
    c6.place(relx= 0.1, rely= 0.55, anchor= 'w')
    c7.place(relx= 0.1, rely= 0.62, anchor= 'w')
    c8.place(relx= 0.1, rely= 0.69, anchor= 'w')

    imgxcoll_ = tk.IntVar(value= 1)
    numofcoll_ = tk.IntVar(value= 1)

    tk.Label(proj, text = 'Images per collage: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.5, rely= 0.33, anchor= 'w')
    imgxcoll = tk.Entry(proj, textvariable = imgxcoll_, font= ('Josefin Slab', 14, 'bold'))
    imgxcoll.place(relx= 0.5, rely= 0.38, anchor= 'w')

    tk.Label(proj, text = 'Number of collages: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.5, rely= 0.5, anchor= 'w')
    numofcoll = tk.Entry(proj, textvariable = numofcoll_, font= ('Josefin Slab', 14, 'bold'))
    numofcoll.place(relx= 0.5, rely= 0.58, anchor= 'w')

    chck_box_ctrols= [c1_,c2_,c3_,c4_,c5_,c6_,c7_,c8_]
    
    generate = tk.Button(proj, text= 'Generate', font= ('Josefin Slab', 14, 'bold'), command= lambda:gen_proj_coll(chck_box_ctrols,imgxcoll_,numofcoll_))
    generate.place(relx= 0.5, rely= 0.74, anchor= 'c')

    bk_button = tk.Button(proj, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= proj.destroy)
    bk_button.place(relx= 0.04, rely= 0.04, anchor= 'nw')


def gen_client_coll(check_box_ctrls,imgxcoll_,numofcoll_,bs4_ratio):

    cat_values = [item.get() for item in check_box_ctrls]
    
    cat_strings = [
            'All_Projects',
            'Architecture',
            'Hotel',
            'Restaurant_Bar',
            'Spa_Wellness',
            'Entertainment',
            'Residential',
            'Masterplan'
            ]

    img_col = imgxcoll_.get()
    num_col = numofcoll_.get()
    ratio = float(bs4_ratio.get())


    # sets the ratio to be scraped from Archilovers
    amount_to_scrap = (img_col*num_col)*ratio
    amount_to_get_from_db = (img_col*num_col)*(1-ratio)
    amount_to_get_from_db = round(amount_to_get_from_db)
    amount_to_scrap = round(amount_to_scrap)

    records = studio_prj_CRUD.load_all_images()

    string_activated = [cat_strings[i] for i, item in enumerate(cat_values) if item==1]
    # print(string_activated,cat_values, len(string_activated))

    # 1 represents the property type
    filtered_img_results = [photo_record[3] for photo_record in records if photo_record[1] in string_activated]
    
    random.shuffle(filtered_img_results)

    #work in bsoup
    """
    filter images from www.archilovers.com/projects?keywords={query_item} for query_item in string_activated

    the ratio is all about getting ex 1/3 filtered_img_resultsof the images from the db, and the quantity that represents the 2/3 take from archi lovers

    and from that list, make a collage
    """    

    results_archilovers_64 = parse_and_save(amount_to_scrap,string_activated)

    print(len(results_archilovers_64))

    from_scrap = results_archilovers_64[:amount_to_scrap//num_col]
    print(f"to this image list pos:{amount_to_scrap//num_col}")

    rest = imgxcoll_.get() - len(from_scrap)
    bs64_to_form = from_scrap + filtered_img_results[:rest]

    for i in range(numofcoll_.get()):
        str_image = collage_obj.create_collage(amount_of_images= len(bs64_to_form), encodings_b64= bs64_to_form)
        
        random.shuffle(results_archilovers_64)
        random.shuffle(filtered_img_results)
        from_scrap = results_archilovers_64[:amount_to_scrap//num_col]
        
        bs64_to_form = from_scrap + filtered_img_results[:rest]
        

        record = {
            'id':None,
            'property_type':'collages.client',
            'location':'none',
            'image_str':str_image
        }
        
        was_inserted = studio_clt_CRUD.insert_image(record)
        
        if was_inserted:
            print(f"collage {i}-th properly save in db")
        else:
            print("Error: collage not saved in db")
    print("done")

def client_coll():
    client = tk.LabelFrame(client_fm, text= ' Add Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    client.pack(fill= 'both', expand= True, padx= 0, pady= 0)

    mult_selec_font = ('Josefin Slab', 12, 'bold')

    lb = tk.Label(client, text= ' Select type of StudioGRONDA project: ', font= mult_selec_font)
    lb.place(relx= 0.1, rely= 0.1, anchor= 'w')

    c1_ = tk.IntVar() # 1 if checkboxed, 0 if not
    c2_ = tk.IntVar()
    c3_ = tk.IntVar()
    c4_ = tk.IntVar()
    c5_ = tk.IntVar()
    c6_ = tk.IntVar()
    c7_ = tk.IntVar()
    c8_ = tk.IntVar()

    c1 = tk.Checkbutton(client, text= 'All Projects', variable= c1_, font= mult_selec_font)
    c2 = tk.Checkbutton(client, text= 'Architecture', variable= c2_, font= mult_selec_font)
    c3 = tk.Checkbutton(client, text= 'Hotel', variable= c3_, font= mult_selec_font)
    c4 = tk.Checkbutton(client, text= 'Restaurant/Bar', variable= c4_, font= mult_selec_font)
    c5 = tk.Checkbutton(client, text= 'Spa/Wellness', variable= c5_, font= mult_selec_font)
    c6 = tk.Checkbutton(client, text= 'Entertainment', variable= c6_, font= mult_selec_font)
    c7 = tk.Checkbutton(client, text= 'Residential', variable= c7_, font= mult_selec_font)
    c8 = tk.Checkbutton(client, text= 'Masterplan', variable= c8_, font= mult_selec_font)

    c1.place(relx= 0.1, rely= 0.2, anchor= 'w')
    c2.place(relx= 0.1, rely= 0.27, anchor= 'w')
    c3.place(relx= 0.1, rely= 0.34, anchor= 'w')
    c4.place(relx= 0.1, rely= 0.41, anchor= 'w')
    c5.place(relx= 0.1, rely= 0.48, anchor= 'w')
    c6.place(relx= 0.1, rely= 0.55, anchor= 'w')
    c7.place(relx= 0.1, rely= 0.62, anchor= 'w')
    c8.place(relx= 0.1, rely= 0.69, anchor= 'w')

    imgxcoll_ = tk.IntVar(value= 1)
    numofcoll_ = tk.IntVar(value= 1)
    bs4ratio = tk.StringVar(value= "0.5")

    tk.Label(client, text = 'Images per collage: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.5, rely= 0.2, anchor= 'w')
    imgxcoll = tk.Entry(client, textvariable= imgxcoll_, font= ('Josefin Slab', 14, 'bold'))
    imgxcoll.place(relx= 0.5, rely= 0.28, anchor= 'w')

    tk.Label(client, text = 'Number of collages: ', font= ('Josefin Slab', 14, 'bold')).place(relx= 0.5, rely= 0.36, anchor= 'w')
    numofcoll = tk.Entry(client, textvariable= numofcoll_, font= ('Josefin Slab', 14, 'bold'))
    numofcoll.place(relx= 0.5, rely= 0.44, anchor= 'w')

    tk.Label(client, text = 'Ratio of Archilover images to \n StudioGRONDA project images: ', font= ('Josefin Slab', 11, 'bold')).place(relx= 0.5, rely= 0.52, anchor= 'w')
    numofcoll = tk.Entry(client, textvariable= bs4ratio, font= ('Josefin Slab', 11, 'bold'))
    numofcoll.place(relx= 0.5, rely= 0.60, anchor= 'w')

    chck_box_ctrols = [c1_,c2_,c3_,c4_,c5_,c6_,c7_,c8_]
    
    generate = tk.Button(client, text= 'Generate', font= ('Josefin Slab', 14, 'bold'), command= lambda: gen_client_coll(chck_box_ctrols,imgxcoll_,numofcoll_, bs4ratio))
    generate.place(relx= 0.5, rely= 0.80, anchor= 'c')

    bk_button = tk.Button(client, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= client.destroy)
    bk_button.place(relx= 0.04, rely= 0.04, anchor= 'nw')

""" TALENT IMAGES MAIN FRAME """

def talent_collage_view():
    global talent_fm

    talent_fm = tk.LabelFrame(mainframe, text= ' Talent Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    talent_fm.pack(fill="both", expand= True, padx= 0, pady= 0)

    b1 = tk.Button(talent_fm, text= 'Add Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= talent_coll)
    b2 = tk.Button(talent_fm, text= 'Visualize Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= lambda: visualize(talent_fm,"talent"))
    b3 = tk.Button(talent_fm, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= talent_fm.destroy)

    b1.place(relx= 0.5, rely= 0.33, anchor= 'center')
    b2.place(relx= 0.5, rely= 0.66, anchor= 'center')
    b3.place(relx= 0.04, rely= 0.04, anchor= 'nw')

""" PROJECT IMAGES MAIN FRAME """

def proj_collage_view():
    global proj_fm
    
    proj_fm = tk.LabelFrame(mainframe, text= ' Project Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    proj_fm.pack(fill="both", expand= True, padx= 0, pady= 0)
    
    b1 = tk.Button(proj_fm, text= 'Add Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= proj_coll)
    b2 = tk.Button(proj_fm, text= 'Visualize Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= lambda: visualize(proj_fm,"proj"))
    b3 = tk.Button(proj_fm, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= proj_fm.destroy)

    b1.place(relx= 0.5, rely= 0.33, anchor= 'center')
    b2.place(relx= 0.5, rely= 0.66, anchor= 'center')
    b3.place(relx= 0.04, rely= 0.04, anchor= 'nw')

""" PROJECT IMAGES MAIN FRAME """

def client_collage_view():
    global client_fm 

    client_fm = tk.LabelFrame(mainframe, text= ' Client Collages ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    client_fm.pack(fill= "both", expand= True, padx= 0, pady= 0)

    b1 = tk.Button(client_fm, text= 'Add Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= client_coll)
    b2 = tk.Button(client_fm, text= 'Visualize Collages', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= lambda: visualize(client_fm,"client"))
    b3 = tk.Button(client_fm, text= '<< Back', height = '1', width = '7', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= client_fm.destroy)

    b1.place(relx= 0.5, rely= 0.33, anchor= 'center')
    b2.place(relx= 0.5, rely= 0.66, anchor= 'center')
    b3.place(relx= 0.04, rely= 0.04, anchor= 'nw')

""" [] MAIN VIEW [] """

def mainview(root):
    global mainframe 

    mainframe = tk.LabelFrame(root, text= ' Please select which category of collages you wish to display or edit: ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    mainframe.pack(fill= "both", expand= True, padx= 8, pady= 8)

    b1 = tk.Button(mainframe, text= 'Talent Images', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= talent_collage_view)
    b2 = tk.Button(mainframe, text= 'StudioGRONDA Project Images', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= proj_collage_view)
    b3 = tk.Button(mainframe, text= 'Firm Client Images', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= client_collage_view)
    b4 = tk.Button(mainframe, text= '<< Logout', height = '1', width = '9', fg= 'white', bg= '#000000', font= ('Josefin Slab', 9, 'bold'), command= lambda: [mainframe.destroy(), root.destroy(), main()])

    b1.place(relx= 0.5, rely= 0.2, anchor= 'center')
    b2.place(relx= 0.5, rely= 0.5, anchor= 'center')
    b3.place(relx= 0.5, rely= 0.8, anchor= 'center')
    b4.place(relx= 0.04, rely= 0.04, anchor= 'nw')

"""" Root Customization """

def root_cust(root):
    global button_font
    
    root.geometry("600x800")
    root.title(' Archivid')

    # app icon 
    #root.iconbitmap('./img/sg_icon.ico')

    # background color
    root.config(background= '#000000',  highlightthickness= 1.5)

    # font
    button_font = font.Font(family= 'Calibri', size= 14, weight= 'bold')

""" [][][] MAIN [][][] """

def main():
    global root 
    global loginframe
    
    # defining root
    root = tk.Tk()

    # customizing root appearance
    root_cust(root)

    loginframe = tk.LabelFrame(root, text= ' Please login or register: ', font= ('Josefin Slab', 9, 'bold'), bg= 'white')
    loginframe.pack(fill="both", expand= True, padx= 8, pady= 8)

    loginframe.update()
    tk.Label(loginframe, text = 'Archivid', bg = 'grey', width= loginframe.winfo_width(), height = '2', font = ('Josefin Slab', 20, 'bold')).place(relx= 0.5, rely= 0.1, anchor= 'center')
    
    b1 = tk.Button(loginframe, text= 'Login', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= login)
    b2 = tk.Button(loginframe, text= 'Register', height = '2', width = '30', fg= 'white', bg= '#000000', font= button_font, command= register)

    b1.place(relx= 0.5, rely= 0.4, anchor= 'center')
    b2.place(relx= 0.5, rely= 0.7, anchor= 'center')

    root.mainloop()

if __name__ == '__main__':
    #if args.download_first:
        #//call scrappers to fill the db
    #else:
        #we asume that our db is filled
    main()
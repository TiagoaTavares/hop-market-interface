#!/usr/bin/env python3
import json
import requests
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import gi

#for opencv
import cv2
import numpy as np
import time

#local
import ipstack

#
gi.require_version('Gtk', '3.0')

API_URL = 'http://api.hopmarket.tk:3000'

# GLOBAL VARS
global login_var
global w_choose
global capture
login_var = False
token = None
w_choose = False
capture = None


# ==============CALLBACKS=========
class CallBacks:

    def __init__(self):
        self.token = None
        self.imageCapture = None
        self.capture = False
        self.products_list=[]

        self.latitude= None
        self.longitude= None

    def login(self, username, password):

        resp = requests.post(f'{API_URL}/auth/login', json={
                      'username': username,
                      'password': password, })

        if resp.status_code != 201:
            raise Exception("could not login")

        token = resp.json()['token']

        self.token = f"Bearer {token}"

        print(self.token)

        return True

    
    def products(self):
        resp = requests.get(f'{API_URL}/products/mine',
                             headers = {'Authorization': f'{self.token}'})
        products = resp.json()

        return products

    # Refreshcombobox
    def Get_products(self):
        
        combobox_type = builder.get_object('type_combo_box')
        
        for item in self.products():
            combobox_type.append_text(item['name'])
            self.products_list.append(item['name'])


    def Check_Fields_Product(self):
        entry_name = builder.get_object('entry_product_name')
        combo_type = builder.get_object('combo_product_type')
        entry_composition = builder.get_object('entry_composition')
        entry_description = builder.get_object('entry_product_description')


        info_label_product= builder.get_object('info_label_product')

        name_product = entry_name.get_text()
        type_product = combo_type.get_active_text()
        description_product = entry_description.get_text()
        composition_product = entry_composition.get_text()


        if name_product and description_product and composition_product:
            print ("tudo preenchido")
            return True

        else:
            info_label_product.set_text("Fill all fields")
            return False
    
    def CreateProduct(self):

        entry_name = builder.get_object('entry_product_name')
        combo_type = builder.get_object('combo_product_type')
        entry_composition = builder.get_object('entry_composition')
        entry_description = builder.get_object('entry_product_description')

        info_label_product= builder.get_object('info_label_product')

        #authorizationHeader = f"Bearer {token}"
        #print(authorizationHeader)

        name_product = entry_name.get_text()
        type_product = combo_type.get_active_text()
        description_product = entry_description.get_text()
        composition_product = entry_composition.get_text()

        
        resp = requests.post(f'{API_URL}/products',
                             json={ 'name': name_product, 'description': description_product},
                             headers = {'Authorization': f'{self.token}'})
        
        print(resp.status_code)
        print(resp.json())

        if resp.status_code == 201:
            info_label_product.set_text("PRODUCT CREATED :)")
        else:
            info_label_product.set_text("FAILED :( try again")
            
    def CreateItem(self):
        combobox_type = builder.get_object('type_combo_box')
        item_activate = combobox_type.get_active_text()
        #print(item)

        idx=0
        print("lista=",self.products_list)
        for item in self.products_list:
            print(idx)
            if item_activate == self.products_list[idx]:
                print("idx=", idx)
                break
            idx=idx+1

        #1: send CREATE ITEM
        resp = requests.post(f'{API_URL}/id',
                             json={ 'productId': idx, 'location': "lat,long"},
                             headers = {'Authorization': f'{self.token}'})
        
        print(resp.status_code)
        print(resp.json())
        
        #2: INFO: created or not created
        
        #3: show QR_code 

    def get_localization(self):
        api_key= '91bcda69858e497e10ec7bcdac3ecbd0'
        geo_lookup = ipstack.GeoLookup(api_key)

        local_info=builder.get_object('label_localization') 

        location = geo_lookup.get_own_location()
        region = location['region_name']
        self.latitude= location['latitude']
        self.longitude= location['longitude']

        local_info.set_text(region)
        print("LOCALIDADE=", region, "latitude=", latitude, "longitude", longitude)

    def show_frame(self,*args):
        
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        # if greyscale:
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        # else:
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])
        image.set_from_pixbuf(pb.copy())
        
        if self.capture:
            self.imageCapture = pb.copy()
            self.capture = False

        return True

    def send_image(self):
        self.capture = True

        while self.capture == False:
            pass

        if self.imageCapture.savev('image.png', 'png', [], []):
        
            response = requests.post(f'{API_URL}/products/photos', 
                                    files=dict(files=open('image.png', 'rb').read()),
                                    headers = {'Authorization': f'{self.token}'})

            print(response.status_code)
        else:
            raise Exception('Error saving')





# =================================HANDLERS==================
# Handler log in
class Handler:

    def __init__(self, callbacks):
        self.callbacks = callbacks

    # ************ HANDLER LOG IN *********
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonOk(self, button):
        print("OK, send data!")

        username = builder.get_object('entry_username').get_text()
        password = builder.get_object('entry_password').get_text()
        print("username=", username)
        print("password=", password)

        # ok = self.callbacks.login(username, password)
        ok = self.callbacks.login("tiago1234", "tiago1234")

        if ok:
            window_login.hide()
            window_choose.show_all()

        # Gtk.main_quit()

    def onButtonCancel(self, button):
        print("Cancel!")
        Gtk.main_quit()

    # ********** HANDLER CHOOSE *****

    def onDestroyChoose(self, *args):
        Gtk.main_quit()

    def onCreateProduct(self, button):
        window_choose.hide()
        window_create_product.show_all()

    def onCreateObjectID(self, button):
        window_choose.hide()
        window_create_objectid.show_all()
        self.callbacks.Get_products()
        self.callbacks.get_localization()

    def onButtonCancelChoose(self, button):
        # print("Cancel!")
        Gtk.main_quit()



    # ********** HANDLER CREATE ObjectID*****
    def onDestroyObjectID_main(self, *args):
        Gtk.main_quit()

    def onCreateObjectID_main(self, button):
        print("CREATE ID")
        self.callbacks.CreateItem()
        # Gtk.main_quit()

    def onButtonBackward_objectid(self, button):
        window_create_objectid.hide()
        window_choose.show_all()

    def on_name_combo_changed(self, combo):
        combo = builder.get_object('type_combo_box')
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            # print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            print("else else")
        
    # ********** HANDLER CREATE PRODUCT*****
    def onDestroyProduct_main(self, *args):
        Gtk.main_quit()

    def onCreateProduct_main(self, button):
        print("CREATE PRODUCT buttom")

        self.callbacks.send_image()

        field=self.callbacks.Check_Fields_Product()

        if field:
            self.callbacks.CreateProduct()
        

    def onButtonBackward_product(self, button):
        window_create_product.hide()
        window_choose.show_all()
        

# --------------------------------------------------------

# builder
builder = Gtk.Builder()
builder.add_from_file("interface.glade")
callbacks = CallBacks()
builder.connect_signals(Handler(callbacks))

# ==========DEF windows===========
window_login = builder.get_object("GTK_window_loggin")
window_choose = builder.get_object("GTK_window_choose")
window_create_product = builder.get_object("GTK_window_createproduct")
window_create_objectid = builder.get_object("GTK_window_createobjectid")
# ---------------------------------------------------
window_login.show_all()  # START first window
#opencv
cap = cv2.VideoCapture(0)
image = builder.get_object("camera_image")

GLib.idle_add(callbacks.show_frame)

Gtk.main()

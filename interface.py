#!/usr/bin/env python3
import json
import requests
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import gi

#for opencv
import cv2
import numpy as np

#
gi.require_version('Gtk', '3.0')


# GLOBAL VARS
global login_var
global token
global w_choose
login_var = False
token = None
w_choose = False


# ==============CALLBACKS=========
class CallBacks:

    # Refreshcombobox
    def Get_products():
        print("refresh combobox")

        combobox_type = builder.get_object('type_combo_box')

        # combobox_type.connect("changed", on_name_combo_changed(combobox_type))

        items = ["item1", "item2", "item3", "item4"]
            
        for item in items:
            combobox_type.append_text(item)

        combobox_type.set_entry_text_column(1)

    # def on_name_combo_changed(combo):
    #     tree_iter = combo.get_active_iter()
    #     if tree_iter is not None:
    #         model = combo.get_model()
    #         row_id, name = model[tree_iter][:2]
    #         print("Selected: ID=%d, name=%s" % (row_id, name))
    #     else:
    #         entry = combo.get_child()
    #         print("Entered: %s" % entry.get_text())

    def Check_Fields_Product():
        entry_name = builder.get_object('entry_product_name')
        entry_type = builder.get_object('entry_product_type')
        entry_description = builder.get_object('entry_product_description')

        info_label_product= builder.get_object('info_label_product')


        if entry_name.get_text() and entry_type.get_text() and entry_description.get_text():
            print ("tudo preenchido")
            return True

        else:
            info_label_product.set_text("Fill all fields")
            return False
    
    def CreateProduct():

        global token

        entry_name = builder.get_object('entry_product_name')
        entry_type = builder.get_object('entry_product_type')
        entry_description = builder.get_object('entry_product_description')

        info_label_product= builder.get_object('info_label_product')

        #authorizationHeader = f"Bearer {token}"
        #print(authorizationHeader)
        
        resp = requests.post('http://api.hopmarket.tk/products',
                             json={ 'name': entry_name.get_text(), 'description': entry_description.get_text()},
                             headers = {'Authorization': f'Bearer {token}'})
        
        print(resp.status_code)
        print(resp.json())

        if resp.status_code == 201:
            info_label_product.set_text("PRODUCT CREATED :)")
        else:
            info_label_product.set_text("FAILED :( try again")
            





# =================================HANDLERS==================
# Handler log in
class Handler:

    # ************ HANDLER LOG IN *********
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonOk(self, button):
        print("OK, send data!")

        entry_username = builder.get_object('entry_username')
        entry_password = builder.get_object('entry_password')
        print("username=", entry_username.get_text())
        print("password=", entry_password.get_text())

        resp = requests.post('http://api.hopmarket.tk/auth/login', json={
                      'username': 'tiago1234',
                      'password': 'tiago1234', })

        if resp.status_code == 201:
            global token
            token = resp.json()['token']
            print(token)
            login_var = True


        if login_var:
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
        CallBacks.Get_products()

    def onButtonCancelChoose(self, button):
        # print("Cancel!")
        Gtk.main_quit()



    # ********** HANDLER CREATE ObjectID*****
    def onDestroyObjectID_main(self, *args):
        Gtk.main_quit()

    def onCreateObjectID_main(self, button):

        print("CREATE ID")
        # Gtk.main_quit()

    def onButtonBackward_objectid(self, button):
        window_create_objectid.hide()
        window_choose.show_all()
        


    # ********** HANDLER CREATE PRODUCT*****
    def onDestroyProduct_main(self, *args):
        Gtk.main_quit()

    def onCreateProduct_main(self, button):
        print("CREATE PRODUCT buttom")

        field=CallBacks.Check_Fields_Product()

        if field:
            CallBacks.CreateProduct()
        

    def onButtonBackward_product(self, button):
        window_create_product.hide()
        window_choose.show_all()
        

# --------------------------------------------------------
# builder
builder = Gtk.Builder()
builder.add_from_file("interface.glade")
builder.connect_signals(Handler())

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

def show_frame(*args):
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    # if greyscale:
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    # else:
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                        GdkPixbuf.Colorspace.RGB,
                                        False,
                                        8,
                                        frame.shape[1],
                                        frame.shape[0],
                                        frame.shape[2]*frame.shape[1])
    image.set_from_pixbuf(pb.copy())
    return True

GLib.idle_add(show_frame)

Gtk.main()

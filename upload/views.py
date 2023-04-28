# CHANGE TEST TO PRODUCTION IN FIREBASE
from django.shortcuts import redirect, render
from upload.forms import UserImage
from .models import UploadImage
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
import json
import base64
import pyrebase 
import os
from datetime import datetime
import random
from .dfuc import dfuc
from django.core.validators import validate_image_file_extension
from .footValid import footValid
from .slic_apply import slic_apply
# declare vals variable to use in results\views.py

config = {
    "apiKey": "AIzaSyDC2DsvGtSfGsLyavQdvpW7oi4BfXtm2RY",
    "authDomain": "diabsense2.firebaseapp.com",
    "databaseURL": "https://diabsense2-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "diabsense2",
    "storageBucket": "diabsense2.appspot.com",
    "messagingSenderId": "611864714060",
    "appId": "1:611864714060:web:88f7e6e0990b5c36304de9"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()
storage = firebase.storage()

data = {}
uploaded = False

def image_request(request):
    if request.method == "POST":
        form = UserImage(request.POST, request.FILES)
        form.save()
        img_object = form.instance
        img_name = str(img_object.image.name)
        
        if form.is_valid() and footValid(img_name):

            slic_apply(img_name)
            # print(type(img_name)

            #removing since redundant copies in sqlite
            a = random.randint(0, 10000)
            #pushing image to cloud storage from local
            sto = storage.child('img_'+str(a)).put(img_object.image)

            # getting probability values

            
            img_url = storage.child('img_'+str(a)).get_url(sto['downloadTokens'])

            # improve this, lags realtime
            dt = datetime.now().strftime("%Y-%M-%D %H:%M:%S")



            # making dictionary of data
            data['img'] = img_url


            set_vals([i for i in dfuc(img_object.image)])

            data['c1'] = vals[0]
            data['c2'] = vals[1]
            data['c3'] = vals[2]
            data['c4'] = vals[3]
            data['date'] = dt

            # pushing data to realtime
            db.push(data)

            # close file object
            img_object.image.close()

            #deleting image from local storage
            delete = default_storage.delete(img_name)

            # close the file path
            uploaded = True

            # link to results page
            return redirect('results')
        else:
            delete = default_storage.delete(img_name)
            messages.success(request,'Not a valid image file')

    form = UserImage()
    return render(request, "image_form.html", {"form": form})

def get_vals():
    return vals

def set_vals(v):
    global vals
    vals = v

def results(request):
    return render(request, "results.html")

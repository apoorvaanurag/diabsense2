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
        if form.is_valid():

            form.save()
            img_object = form.instance
            a = random.randint(0, 10000)
            #pushing image to cloud storage from local
            sto = storage.child('img_'+str(a)).put(img_object.image)

            # getting probability values

            
            img_url = storage.child('img_'+str(a)).get_url(sto['downloadTokens'])

            dt = datetime.now().strftime("%Y-%M-%D %H:%M:%S")



            # making dictionary of data
            data['img'] = img_url


            vals = dfuc(img_object.image)
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
            img_name = str(img_object.image.name)
            delete = default_storage.delete(img_name)

            # close the file path
            messages.success(request, "File upload in Firebase Storage successful")
            uploaded = True

            return render(
                request, "image_form.html", {"form": form, "img_obj": img_object, "up":uploaded}
            )
    else:
        form = UserImage()

    return render(request, "image_form.html", {"form": form})

def results(request):
    
    return render(request, "results.html")




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
from .convert_to_square_image import convert_to_square_image
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#pull config from .config and save it to config variable

config = json.load(open('.config'))

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()
storage = firebase.storage()

data = {}

def image_request(request):
    if request.method == "POST":
        set_uploaded(False)
        form = UserImage(request.POST, request.FILES)
        # logging.info('User has uploaded an image')
        form.save()
        img_object = form.instance
        img_name = str(img_object.image.name)

        if form.is_valid():
            # logging.info('Image has been validated')

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


            # convert to square image
            convert_to_square_image(img_name)

            # apply slic
            slic_apply(img_name)

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

            # uploaded = True
            set_uploaded(True)

            # link to results page
            return redirect('results')
        else:
            logging.info('Image has failed validation')
            # delete = default_storage.delete(img_name)
            messages.success(request,'Not a valid image file')

    form = UserImage()
    return render(request, "image_form.html", {"form": form})

def get_vals():
    return vals

def set_vals(v):
    global vals
    vals = v

def get_uploaded():
    return uploaded

def set_uploaded(u):
    global uploaded
    uploaded = u
    # logging.info('Upload set to: '+str(get_uploaded()))

def results(request):
    return render(request, "results.html")

from tensorflow import keras
import numpy as np
import os
import base64
from PIL import Image
from io import BytesIO
from google.cloud import storage
from flask import jsonify, make_response


BUCKET_NAME        = "fatigue-detection"
PROJECT_ID         = "face-to-face-fatigue"
GCS_MODEL_FILE     = "fatigue.h5"
# Initialise a client
client   = storage.Client(PROJECT_ID)    

bucket   = client.get_bucket(BUCKET_NAME)
    
blob     = bucket.blob(GCS_MODEL_FILE)
    
folder = '/'
if not os.path.exists(folder):
    os.makedirs(folder)

blob.download_to_filename(folder + "fatigue.h5")

# global model
# if not model:
#     download_model_file()
#     model = load_model("/tmp/fatigue.h5")

class Classification():
    def _init_(self,imgstr,filename):
        self.model = keras.models.load_model(os.path.join(os.getcwd(),'api','fatigue.h5'))
        self.imgstr = imgstr
        self.filename = filename
        self.img = ""

    def classify(self):
        x = np.array(self.img)
        x = x / 255
        x = np.expand_dims(x, axis=0)
        img = np.vstack([x])
        hasil = self.model.predict(img, batch_size=10)
        #print(hasil)
        hasil = ['flefteye', 'fmouth', 'frighteye', 'nlefteye', 'nmouth', 'nrighteye']
        # return hasil[np.argmax(classes)]
        json_hasil = hasil[np.argmax(classes)]
        return jsonify(result = json_hasil)
    
    def decode(self):
        image_in_string = base64.b64decode(self.imgstr)
        image = Image.open(BytesIO(image_in_string)).resize((150,150)).convert("RGB")
        self.img = image
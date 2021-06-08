from flask import Flask,request,jsonify
import os
from werkzeug.utils import secure_filename
from Classifier import Classification

PATH = os.getcwd()
IMAGE_LOCATION = os.path.join(PATH,"images")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__, static_url_path='/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict/', methods=['POST'])
def upload():
        respond = []
        if request.method == 'POST':
            if not request.json.get("image") or request.json.get("image") is None:
                respond.append({
                    "message":"image not found"
                })
                return jsonify(respond)
            if not request.json.get("filename") or request.json.get("filename") is None :
                respond.append({
                    "message":"filename not found"
                })
                return jsonify(respond)
            filename = request.json.get("filename")
            imgstring = request.json.get("image")
            if imgstring and allowed_file(filename):
                filename = secure_filename(filename)
                classification = Classification(imgstring,filename)
                classification.decode()
                confident,verdict = classification.classify()
                respond.append({
                    "filename":filename,
                    "confidentLevel":confident,
                    "verdict":verdict,
                })
            else:
                respond.append({
                "message":"type file not permitted"
                })
        else:
            respond.append({
                "message":"request error"
            })
        return jsonify(respond)

if _name_ == "_main_":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 443))
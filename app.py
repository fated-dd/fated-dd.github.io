
from flask import Flask , render_template , request , url_for , redirect
from sympy.polys.polyoptions import Method
from app4flask import process
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/static/forupload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    # image = map()
    # result = main_app(image)
    return render_template('index.html')

@app.route('/' , methods = ["GET" , "POST"])
def transfer():
    if Method == "POST":
        pass

if __name__ == '__main__':
    app.run(debug = True)

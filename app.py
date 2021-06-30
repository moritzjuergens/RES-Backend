from flask import *

import os
import res as test
from flask_cors import CORS
from werkzeug.utils import secure_filename


key = os.urandom(24)
app.secret_key = key
app = Flask(__name__)

cors = CORS(app, resources={r"/": {"origins": "https://testt.tiiny.site/"}})

ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 



PRE = [
    
]  


@app.route('/')
def hello():
    return redirect("https://testt.tiiny.site/", code=302)

@app.route('/send', methods=['POST'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def foo():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        #os.rename(uploaded_file.filename, 'cv.pdf')
        test.cleaning_json()
        test.pdf_to_json(uploaded_file.filename)
        test.run()
        result = test.run()
        test.get_job()
        #test.cleaning_json()
    return render_template("layout.html", result = result) 


@app.route('/jobs')
def presets():
    #post_data = request.get_json()
    return test.get_job()

if __name__ == '__main__':
    app.run(debug=True, port=33507)

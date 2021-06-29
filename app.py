from flask import *

import os
import res as res
from flask_cors import CORS
from werkzeug.utils import secure_filename


key = os.urandom(24)
app.secret_key = key
app = Flask(__name__)

# allow front end
# front end site   #https://hopeful-hermann-97c612.netlify.app/
cors = CORS(app, resources={r"/": {"origins": "*"}})

# allow only pdf
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# home route => redirect to front end
@app.route('/')
def hello():
    # front end site
    return redirect("https://hopeful-hermann-97c612.netlify.app/", code=302)


UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# send => run our code (algor)
@app.route('/send', methods=['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def run():
    print(' * received form with', list(request.form.items()))
    # get the uploaded file
    for uploaded_file in request.files.getlist('files'):
        print("* recieved: " + uploaded_file.filename)
        if uploaded_file and uploaded_file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            print('* file uploaded', filename)

            uploaded_file.save(uploaded_file.filename)
            #os.rename(uploaded_file.filename, 'cv.pdf')
            # delte old json content
            res.cleaning_json()
            # convert pdf to json
            res.pdf_to_json(uploaded_file.filename)
            # knn classifier
            # res.run()
            category = res.run()
            res.get_job()
        # test.cleaning_json()
    return render_template("layout.html", result=category)


# get the jobs of  the result catogray and return as json structure for the front end
@app.route('/jobs')
def getjOB():
    #post_data = request.get_json()
    return res.get_job()


if __name__ == '__main__':
    app.run(debug=True)

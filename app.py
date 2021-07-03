from flask import *

import os
from flask_cors import CORS
import res as res
from werkzeug.utils import secure_filename


key = os.urandom(24)
app.secret_key = key
app = Flask(__name__)
app.config.from_object(__name__)

# allow front end
# front end site   #https://hopeful-hermann-97c612.netlify.app/
CORS(app, resources={r'/*': {'origins': '*'}})




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# home route => redirect to front end
@app.route('/')
def hello():
    # front end site
    return redirect("https://hopeful-hermann-97c612.netlify.app/", code=302)


UPLOAD_FOLDER = 'uploaded_files'
# allow only pdf
ALLOWED_EXTENSIONS = {'pdf'}
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
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
        print(' * recieved:', uploaded_file.filename)
        if uploaded_file and uploaded_file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            print(' * file uploaded', filename)

            # delete old json content
            res.cleaning_json()
            # convert pdf to json
            res.pdf_to_json("uploaded_files/"+uploaded_file.filename)
            # knn classifier
            category = res.run()

            print(category)

    return category


# get the jobs of  the result catogray and return as json structure for the front end
@app.route('/jobs', methods=['POST'])
def getjOB():

    r = request.json
    print("r:", r)
    #get the jobtitle  and location from the front end
    job = r['jobtitle']
    location = r['location']
    #get the job listing result as json 
    return jsonify(res.get_job(job, location))
    


if __name__ == '__main__':
    #app.run(debug=true)  #for local use
    app.run(host="0.0.0.0")   #for production 

from flask import *
from flask_cors import CORS
import os
from shutil import move
from werkzeug.utils import secure_filename
# from logic_res import run
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def upload():
    return render_template("index.html")

# sanity check route


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET'])
def all_books():
    return jsonify({
        'status': 'success',
        'books': BOOKS
    })


PRE = [
    {
        'title': 'Full-Stack-Developer',
        'config': 'Jack Kerouac',
        'file': 'bro',
        'read': True
    },
    {
        'title': 'Manager',
        'config': 'Jack Kerouac',
        'file': '',
        'read': True
    },
    {
        'title': 'Scrum Master',
        'config': 'Jack Kerouac',
        'file': '',
        'read': True
    },
]


@app.route('/pre', methods=['GET', 'POST'])
def presets():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        PRE.append({
            'title': post_data.get('title'),
            'config': post_data.get('config'),
            'file': post_data.get('file'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['pre'] = PRE
    return jsonify(response_object)


UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/file', methods=['POST'])
def upload_file():
    print(' * received form with', list(request.form.items()))
    # check if the post request has the file part
    for file in request.files.getlist('files'):
        print(file.filename)
        if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            print(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(' * file uploaded', filename)
    return redirect('/')

# @app.route('/success', methods=['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         if(allowed_file(f.filename)):
#             f.save(f.filename)
#             os.rename(f.filename, 'cv.pdf')
#             run()

#             return render_template("layout.html", name=f.filename)
#         else:
#             return "file not supported"


# ALLOWED_EXTENSIONS = {'pdf'}


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/')
# def upload():
#     return render_template("index.html")


# @app.route('/success', methods=['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         if(allowed_file(f.filename)):
#             f.save(f.filename)
#             os.rename(f.filename, 'cv.pdf')
#             run()
#             select = request.form.get('comp_select')
#             return render_template("layout.html", name=f.filename, select=select)
#         else:
#             return render_template("404.html", variable="file not suppored")


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)

from flask import *
from flask_cors import CORS
import os
from shutil import move
from werkzeug.utils import secure_filename
# from logic_res import run
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

ALLOWED_EXTENSIONS = set(['pdf', 'txt'])

UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload():
    return render_template("index.html")

# sanity check route


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


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


@app.route('/file', methods=['POST'])
def upload_file():
    print(' * received form with', list(request.form.items()))
    # check if the post request has the file part
    for file in request.files.getlist('files'):
        if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
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


if __name__ == '__main__':
    app.run(debug=True)

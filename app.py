from flask import *
from flask_cors import CORS
import os
from shutil import move
# from logic_res import run
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        'read': True
    },
    {
        'title': 'Manager',
        'config': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Scrum Master',
        'config': 'Jack Kerouac',
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
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['pre'] = PRE
    return jsonify(response_object)


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

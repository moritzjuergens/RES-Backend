from flask import *  
import os
from logic_res import run




app = Flask(__name__)  


ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 



@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        if(allowed_file(f.filename)):
            f.save(f.filename)  
            os.rename(f.filename, 'cv.pdf')
            run()
            select = request.form.get('comp_select')
            return render_template("layout.html", name = f.filename, select = select)  
        else:
            return render_template("404.html",variable="file not suppored")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/png')
if __name__ == '__main__':  
    app.run(debug = True)  


from flask import Flask, flash, request, redirect, url_for,render_template,session,send_from_directory
import os,glob
import shutil
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import importing_haar_cascade
from PIL import Image

app = Flask(__name__)
Bootstrap(app)
# app.config['BOOTSTRAP_SERVE_LOCAL']=True

app.secret_key = 'sudip'

UPLOAD_FOLDER = 'E:/Emotion-Recognition-master'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    session.pop('messages',None)
    session.pop('images',None)
    # session['prediction']= prediction
    for root, dirs, files in os.walk('./testing'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    for root, dirs, files in os.walk('./static/images'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))        
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
                for root, dirs, files in os.walk('./testing'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

                for root, dirs, files in os.walk('./static/images'):
                     for f in files:
                        os.unlink(os.path.join(root, f))
                for d in dirs:
                     shutil.rmtree(os.path.join(root, d))
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                predictions = importing_haar_cascade.crop_image(filename);
                session['messages'] = predictions
                images = os.listdir(os.path.join(app.static_folder, "images"))
                session['images'] = images
                return redirect(url_for('predict',filename=filename));
    return render_template('upload.html')

@app.route('/predict/<filename>',methods = ['GET','POST'])
def predict(filename):
    # return render_template('portfolio.html', images=images)
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    messages= session['messages']
    images = session['images']
    return render_template('show.html',messages=messages,images=images,zip=zip,filename=filename)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/train_predict')
def train_predict():
    importing_haar_cascade.trains()
    # flash("Emotion Trained Successfully")
    # print(prediction)
    return redirect(url_for('upload_file'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/music')
def music():
    messages = session['messages']
    return render_template('music.html',messages=messages)

@app.route('/jokes')
def jokes():
    messages = session['messages']
    return render_template('jokes.html',messages=messages)        
@app.route('/about')
def about():
    return render_template('about.html')    

@app.route('/train')
def train():
    return render_template('train.html')    


if __name__ == '__main__':
    app.run(debug=True)

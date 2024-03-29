from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import os

app = Flask(__name__)
dropzone = Dropzone(app)


app.config['SECRET_KEY'] = 'secretkey'


app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'


app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  


@app.route('/', methods=['GET', 'POST'])
def index():
    
    
    if "file_urls" not in session:
        session['file_urls'] = []
    
    file_urls = session['file_urls']

    
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
           
            filename = photos.save(
                file,
                name=file.filename    
            )

            
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
        
    return render_template('index.html')


@app.route('/results')
def results():
    
    
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('pictures.html', file_urls=file_urls)

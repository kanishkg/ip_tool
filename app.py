#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask import flash,send_from_directory
from flask import redirect, url_for, jsonify
from werkzeug.utils import secure_filename

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os

import cv2
from ip_scripts.selective_blur import selective_blur
from ip_scripts.inpaint import inpaint_image
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
UPLOAD_FOLDER = '/Users/kanishkgandhi/Documents/coursework/ee604/flask-boilerplate/uploads'
ALLOWED_EXTENSIONS = set([  'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


# @app.route('/')
# def home():
#     return render_template('pages/placeholder.home.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print 'starting'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            return render_template(
            'forms/home.html',filename=filename ,target=filename)
    return render_template(
            'forms/home.html',filename='temp.jpg',target='temp.jpg')

@app.route('/upload',methods=['GET','POST'])
def upload_ajax():
    if request.method == 'POST':
        print "upp"
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print "saved"
            return jsonify({'url':'/uploads/'+filename})
    return

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/blur',methods=['POST'])
def blur_image():
    print 'blurring'
    if request.method =='POST':

        img_loc = request.form['imgsrc']
        print img_loc
        filename = img_loc.split('/')[-1]
        image = cv2.imread(img_loc[1:])
        p2 = [int(float(x)) for x in request.form['p2'].split(':')]
        p1 = [int(float(x)) for x in request.form['p1'].split(':')]
        if request.form['m'] =='1':
            image = selective_blur(image,'ss',p1,p2)
        else:
            image = selective_blur(image,'gc',p1,p2)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],
                                 filename[:-4]+'targetb.jpg'),image)
        target = filename[:-4]+'targetb.jpg'

        return jsonify({'url':'/uploads/'+target})
    return

@app.route('/inpaint',methods=['POST'])
def inpaint():
    print 'blurring'
    if request.method =='POST':

        img_loc = request.form['imgsrc']
        print img_loc
        filename = img_loc.split('/')[-1]
        image = cv2.imread(img_loc[1:])
        p2 = [int(float(x)) for x in request.form['p2'].split(':')]
        p1 = [int(float(x)) for x in request.form['p1'].split(':')]
        if request.form['m'] =='1':
            image = inpaint_image(image,'ss',p1,p2)
        else:
            image = inpaint_image(image,'gc',p1,p2)
        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],
                                 filename[:-4]+'targeti.jpg'),image)
        target = filename[:-4]+'targeti.jpg'

        return jsonify({'url':'/uploads/'+target})
    return



@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

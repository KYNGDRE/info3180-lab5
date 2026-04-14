"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import flash, render_template, request, jsonify, send_file
import os
from app.forms import MovieForm
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import jsonify 
from app.models import Movies
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form=MovieForm()
    print('LOL')
    if form.validate_on_submit():

        # process the data
        title=form.title.data    
        description=form.description.data   
        photo=form.poster.data
           
        print('LOL2')      
        filename = secure_filename(photo.filename)
        print("UPLOAD FOLDER:", app.config.get('UPLOAD_FOLDER'))
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("Saving to:", path)

        photo.save(path)
        date = datetime.now()
        # Get file data and save to your uploads folder
        flash('File Saved', 'success')
        movie = Movies(title=title, description=description, poster=filename, created_at=date)
        db.session.add(movie)         
        db.session.commit()

        responce=[{ "message": "Movie Successfully added",
                             "title": title, 
                             "poster": filename, 
                             "description": description }]
        print(responce)
        return jsonify({ "message": "Movie Successfully added",
                             "title": title, 
                             "poster": filename, 
                             "description": description }), 200
        # return redirect(url_for('dis_props'))
    else:
        errors=form_errors(form)
        print("FORM ERRORS:", errors)
        # responce={"errors": errors}
        return jsonify(errors=errors),400


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
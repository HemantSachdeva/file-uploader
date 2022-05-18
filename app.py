import os

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['file']
        filename = secure_filename(file.filename)
        path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_to_file)
        return render_template('upload.html', filename=filename)


class UploadForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload')


if __name__ == '__main__':
    app.run()

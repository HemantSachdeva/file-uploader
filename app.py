import os

from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, validators

from database.client import UploaderClient
from database.enter_record import enter_record

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16GB


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_name = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)
        metadata = UploaderClient(
            'http://localhost:1080/files/', file_path).upload_to_s3()
        enter_record(metadata)
        print(metadata)
        return render_template('upload.html')
    return render_template('upload.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    form = DownloadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = request.form['text']
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    return render_template('download.html', form=form)


@app.route('/download/<filename>')
def download_file(filename):
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return 'File does not exist'


class DownloadForm(FlaskForm):
    text = StringField('Text', [validators.InputRequired()], render_kw={
                       "placeholder": "Enter file name"})
    submit = SubmitField('Download')


if __name__ == '__main__':
    app.run()

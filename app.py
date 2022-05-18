import os

from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from wtforms import FileField, StringField, SubmitField, validators

from database.enter_record import enter_record

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = request.files['file']
            filename = secure_filename(file.filename)
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_to_file)
            enter_record(path_to_file)
            return render_template('upload.html', filename=filename)
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


class UploadForm(FlaskForm):
    file = FileField('File', validators=[validators.InputRequired()])
    submit = SubmitField('Upload')


class DownloadForm(FlaskForm):
    text = StringField('Text', [validators.InputRequired()], render_kw={
                       "placeholder": "Enter file name"})
    submit = SubmitField('Download')


if __name__ == '__main__':
    app.run()

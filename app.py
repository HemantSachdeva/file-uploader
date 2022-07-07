from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from resources.api.file_upload import Upload

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16GB

api.add_resource(Upload, '/upload/file/s3')

if __name__ == '__main__':
    app.run()

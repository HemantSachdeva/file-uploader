from os import getenv

from dotenv import load_dotenv
from flask import jsonify, request
from models.client import UploaderClient

load_dotenv()

class UploadFileToS3:
    @classmethod
    def upload_file(cls):
        try:
            file = request.files['file']
            cl = UploaderClient(getenv('BUCKET_URL'), file)
            upload_url = cl.upload_to_s3()

            return jsonify({
                'status': 'success',
                'upload_url': upload_url
            })

        except Exception as e:
            print(e)
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

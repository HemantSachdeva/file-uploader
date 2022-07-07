from os import getenv

from dotenv import load_dotenv
from flask import jsonify, request
from models.client import UploaderClient
from models.enter_record import enter_record

load_dotenv()


class UploadFileToS3:
    @classmethod
    def upload_file(cls):
        try:
            file = request.files['file']
            cl = UploaderClient(getenv('BUCKET_URL'), file)
            metadata = cl.upload_to_s3()

            enter_record(metadata)

            return jsonify({
                'status': 'success',
                'metadata': metadata
            })

        except Exception as e:
            print(e)
            return jsonify({
                'status': 'error',
                'message': str(e)
            })

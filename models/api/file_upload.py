from flask import jsonify, request
from models.client import UploaderClient


class UploadFileToS3:
    @classmethod
    def upload_file(cls):
        try:
            file = request.files['file']
            cl = UploaderClient('http://0.0.0.0:1080/files/',
                                file)
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

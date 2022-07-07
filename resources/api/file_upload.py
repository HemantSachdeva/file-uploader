from flask import jsonify
from flask_restful import Resource
from models.api.file_upload import UploadFileToS3


class Upload(Resource):
    @classmethod
    def post(cls):
        data = UploadFileToS3.upload_file().get_json()

        if data['status'] == 'success':
            return jsonify({
                'status': 'success',
                'metadata': data['metadata']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': data['message']
            })

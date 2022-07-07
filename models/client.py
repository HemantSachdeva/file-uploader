"""
 Copyright (C) 2022 Hemant Sachdeva <hemant.evolver@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

from json import loads
import os

import magic
from tusclient import client
from tusclient.storage import filestorage
from tusclient.uploader import Uploader


class UploaderClient:
    """
    Object representation of Tus client.

    :Attributes:
        - url (str):
            represents the S3 bucket's create extension url. On instantiation this argument
            must be passed to the constructor.
        - file (FileStorage):
            Object of the file received in the request.

    :Constructor Args:
        - url (str)
    """

    def __init__(self, url, file):
        self.url = url
        self.file = file

    def get_metadata(self, file):
        """
        Get metadata of the file.

        :Attributes:
            - file (FileStorage):
                Object of the file received in the request.

        :Returns:
            - metadata (dict):
                metadata of the file.
        """

        file_name = file.filename
        extension = file_name.split('.')[-1]
        content_type = magic.from_buffer(file.read(), mime=True)
        file_size = file.seek(0, 2)

        if file_size < 1024:
            file_size = str(file_size) + ' B'
        elif file_size < 1048576:
            file_size = str(round(file_size / 1024, 2)) + ' KB'
        elif file_size < 1073741824:
            file_size = str(round(file_size / 1048576, 2)) + ' MB'
        else:
            file_size = str(round(file_size / 1073741824, 2)) + ' GB'

        metadata = {
            'filename': file_name,
            'extension': extension,
            'content-type': content_type,
            'size': f'{file_size}'
        }

        return metadata

    def upload_to_s3(self):
        """
        Upload a file to S3 bucket.

        :Returns:
            - url (str):
                download url of the uploaded file.
        """

        metadata = self.get_metadata(self.file)

        my_client = client.TusClient(self.url)

        upload_url = filestorage.FileStorage('url.json')
        uploader = Uploader(client=my_client, store_url=True,
                            url_storage=upload_url, file_stream=self.file)
        uploader.upload()

        data = loads(open('url.json').read())

        metadata['url'] = data['_default']['1']['url']

        if os.path.exists('url.json'):
            os.remove('url.json')

        return metadata

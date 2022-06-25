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
from os import path

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
        - file_path (str):
            path of the file to upload.

    :Constructor Args:
        - url (str)
    """

    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def get_metadata(self, file_path):
        """
        Get metadata of the file.

        :Attributes:
            - file_path (str):
                path of the file to get metadata.

        :Returns:
            - metadata (dict):
                metadata of the file.
        """

        file_name = path.basename(file_path)
        extension = file_name.split('.')[-1]
        content_type = magic.from_file(file_path, mime=True)
        file_size = path.getsize(file_path)

        if file_size < 1024:
            file_size = str(file_size) + 'B'
        elif file_size < 1048576:
            file_size = str(round(file_size / 1024, 2)) + 'KB'
        elif file_size < 1073741824:
            file_size = str(round(file_size / 1048576, 2)) + 'MB'
        else:
            file_size = str(round(file_size / 1073741824, 2)) + 'GB'

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

        metadata = self.get_metadata(self.file_path)

        my_client = client.TusClient(self.url)

        upload_url = filestorage.FileStorage('url.json')
        uploader = Uploader(client=my_client, store_url=True, url_storage=upload_url, file_stream=open(file=self.file_path, mode='rb'))
        uploader.upload()

        data = loads(open('url.json').read())
        l = len(data['_default'])

        metadata['url'] = data['_default'][f'{l}']['url']
        return metadata

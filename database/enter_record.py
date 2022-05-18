import os

from magic import Magic

from database.create_table import create_table
from database.db import Connection


def enter_record(path_to_file):
    try:
        connection = Connection.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            magic = Magic(mime=True)
            filename = os.path.basename(path_to_file)
            file_type = magic.from_file(path_to_file)
            file_size = os.path.getsize(path_to_file)
            create_table()
            cursor.execute("INSERT INTO uploads(file_name, URL, file_type, file_size) VALUES(%s, %s, %s, %s)",
                           (filename, 'http://penzl-file-uploader.herokuapp.com/download/' + filename, file_type, file_size))
            connection.commit()
            cursor.close()
            connection.close()
            print("Record inserted successfully into uploads table")
    except Exception as e:
        print("Error while reading records", e)

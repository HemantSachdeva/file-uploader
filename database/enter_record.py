from database.create_table import create_table
from database.db import Connection


def enter_record(metadata):
    """
    Inserts a record into the database.

    :Attributes:
        - metadata (dict):
            metadata of the file.
    """
    try:
        connection = Connection.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            create_table()
            cursor.execute("INSERT INTO uploads(file_name, URL, file_type, file_size) VALUES(%s, %s, %s, %s)",
                           (metadata.get('filename'), metadata.get('url'), metadata.get('content-type'), metadata.get('size')))
            connection.commit()
            cursor.close()
            connection.close()
            print("Record inserted successfully into uploads table")
    except Exception as e:
        print("Error while reading records", e)

import os

from dotenv import load_dotenv
from mysql.connector import Error, connect

load_dotenv()


class Connection:
    def get_connection():
        try:
            connection = connect(user=os.getenv('USERNAME'),
                                 password=os.getenv('PASSWORD'),
                                 database=os.getenv('DB'),
                                 host=os.getenv('HOSTNAME'))
            if connection.is_connected():
                return connection
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None

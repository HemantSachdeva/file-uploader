from models.db import Connection


def create_table():
    try:
        connection = Connection.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS uploads(id INT AUTO_INCREMENT PRIMARY KEY, "
            "file_name VARCHAR(255), "
            "URL VARCHAR(255), "
            "file_type VARCHAR(255), "
            "file_size VARCHAR(255), "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error while creating table", e)

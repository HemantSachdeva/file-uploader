from flask import Flask

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16GB


if __name__ == '__main__':
    app.run()

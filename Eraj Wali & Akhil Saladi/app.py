import os
from flask import send_from_directory
from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')
@app.route("/mediapipe/<path:filename>")
def mediapipe_files(filename):
    return send_from_directory(os.path.join(app.root_path, "static", "mediapipe"), filename)
@app.route('/')
def index():
    return render_template('keyboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

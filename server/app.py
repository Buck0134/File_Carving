from flask import Flask, render_template, jsonify
from forensics_Processor import getFileBasics, get_file_md5_md5
import os
print("Current Working Directory:", os.getcwd())


app = Flask(__name__, template_folder='../client/templates')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def data():
    file_name = "files/example.txt"
    # msg = getFileBasics(file_name)
    msg = get_file_md5_md5(file_name)
    return jsonify({'message': msg})

if __name__ == '__main__':
    app.run(debug=True)

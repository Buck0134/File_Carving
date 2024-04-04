from forensics_Processor import FileHandler
from flask import Flask, render_template, request, jsonify, abort
from werkzeug.utils import secure_filename
import os
import hashlib
import shlex  # For safely creating argument lists
import subprocess

app = Flask(__name__, template_folder='../client/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/file-md5', methods=['GET'])
def file_md5():
    file_path = request.args.get('file_path', '')
    try: 
        if not os.path.isabs(file_path) or os.path.normpath(file_path) != file_path:
                raise ValueError("Path must be an absolute and normalized path")
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Calculate MD5
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
                md5_hash = hashlib.md5(file_bytes).hexdigest()
            return jsonify({'md5': md5_hash})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
    

@app.route('/api/mmls-info', methods=['GET'])
def mmls_info():
    file_path = request.args.get('file_path', '')
    
    try:
        # Ensure the path is within our base directory to prevent Directory Traversal
        if not os.path.isabs(file_path) or os.path.normpath(file_path) != file_path:
            raise ValueError("Path must be an absolute and normalized path")

        # Run the mmls command
        result = subprocess.run(['mmls', file_path], capture_output=True, text=True)
        print(result)
        if result.returncode == 0:
            # Successfully executed mmls
            return jsonify({'info': result.stdout})
        else:
            # mmls command failed
            return jsonify({'error': 'Failed to get MMLS info', 'details': result.stderr}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
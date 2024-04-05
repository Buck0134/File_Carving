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
    
    def parse_mmls_output(output):
        # Split output into metadata and sector info
        meta_lines, sector_lines = output.strip().split('\n\n', 1)
        # Parse sectors
        sectors_info = []
        for line in sector_lines.split('\n')[1:]:
            parts = line.split(maxsplit=5)
            if len(parts) == 6:
                sector_info = {
                    'Index': parts[0],
                    'Slot': parts[1],
                    'Start': parts[2],
                    'End': parts[3],
                    'Length': parts[4],
                    'Description': parts[5]
                }
                sectors_info.append(sector_info)

        return meta_lines, sectors_info
    
    try:
        # Path validation to prevent Directory Traversal
        if not os.path.isabs(file_path) or os.path.normpath(file_path) != file_path:
                    raise ValueError("Path must be an absolute and normalized path")
        
        # Execute mmls command
        result = subprocess.run(['mmls', file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            metadata, sectors_info = parse_mmls_output(result.stdout)
            print(jsonify({'metadata': metadata, 'sectors_info': sectors_info}))
            return jsonify({'metadata': metadata, 'sectors_info': sectors_info})
        else:
            return jsonify({'error': 'Failed to get MMLS info', 'details': result.stderr}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
from forensics_Processor import FileHandler
from flask import Flask, render_template, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
import os
import hashlib
import shlex  # For safely creating argument lists
import subprocess
import tempfile


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
        print(sector_lines)
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
            # print({'metadata': metadata, 'sectors_info': sectors_info})
            return jsonify({'metadata': metadata, 'sectors_info': sectors_info})
        else:
            return jsonify({'error': 'Failed to get MMLS info', 'details': result.stderr}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

@app.route('/api/extract-data-to-local', methods=['POST'])
def extract_data_to_local():
    print("TEST")
    # Extract parameters from POST request
    file_path = request.json.get('file_path')
    start_sector = request.json.get('start_sector')
    length = request.json.get('length')
    byte_size = request.json.get('byte_size', 512)  # Default byte size is 512

    # Basic input validation
    if not all([file_path, start_sector, length, byte_size]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Sanitize inputs
        file_path = shlex.quote(file_path)
        start_sector = int(start_sector)
        length = int(length)
        byte_size = int(byte_size)
        skip = start_sector

        # Ensure file_path is safe and exists
        if not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Define output directory within the specified path
        base_dir = os.path.dirname(file_path)
        output_dir = os.path.join(base_dir, 'File_Carving_Carved_out_DD')
        os.makedirs(output_dir, exist_ok=True)

        # Define output file path
        output_file = os.path.join(output_dir, f"carved_{os.path.basename(file_path)}")

        # Construct and execute dd command
        dd_command = f"dd if={file_path} of={output_file} bs={byte_size} count={length} skip={skip}"
        result = subprocess.run(dd_command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': 'dd command failed', 'details': result.stderr}), 500

        # Return success response
        return jsonify({'message': 'Data extracted successfully', 'output_file': output_file})

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

@app.route('/api/extract-data-to-download', methods=['POST'])
def extract_data_to_download():
    # Extract parameters from POST request
    file_path = request.json.get('file_path')
    start_sector = request.json.get('start_sector')
    length = request.json.get('length')
    byte_size = request.json.get('byte_size', 512)  # Default byte size is 512
    # Basic input validation
    if not all([file_path, start_sector, length, byte_size]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Sanitize inputs to prevent command injection
        file_path = shlex.quote(file_path)
        start_sector = int(start_sector)
        length = int(length)
        byte_size = int(byte_size)
        skip = start_sector

        # Ensure file_path is safe (additional checks might be needed)
        if not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Create a temporary file to hold the extracted data
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        # Construct dd command
        dd_command = f'dd if={file_path} of={temp_file.name} bs={byte_size} count={length} skip={skip}'

        # Execute dd command
        result = subprocess.run(dd_command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': 'dd command failed', 'details': result.stderr}), 500

        # Return the path or contents of the temporary file
        # Note: Returning file contents directly might not be feasible for large files
        return send_file(temp_file.name, as_attachment=True)

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
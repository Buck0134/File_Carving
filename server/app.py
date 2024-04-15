from forensics_Processor import FileHandler
from flask import Flask, render_template, request, jsonify, abort, send_file
from werkzeug.utils import secure_filename
import os
import hashlib
import shlex  # For safely creating argument lists
import subprocess
import tempfile
import re


app = Flask(__name__, template_folder='../client/templates')

@app.route('/')
def home():
    return render_template('index.html')

def check_if_sector_is_filesystem(file_path, sector_start):
    # Build fls command with offset
    cmd = ['fls', '-o', str(sector_start), file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # If command executes successfully, it's likely a file system
    return result.returncode == 0

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

    def check_if_sector_is_filesystem(file_path, sector_start):
        # Ensure sector_start is a number
        if not sector_start.isdigit():
            return False
        # fls requires the sector offset to be passed as a sector unit, calculate it
        sector_offset = int(sector_start)  # Assuming 512 bytes per sector
        cmd = ['fls', '-o', str(sector_offset), file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def parse_mmls_output(output):
        # Split output into metadata and sector info
        meta_lines, sector_lines = output.strip().split('\n\n', 1)
        # Parse sectors
        print(sector_lines)
        sectors_info = []
        for line in sector_lines.split('\n')[1:]:
            parts = line.split(maxsplit=5)
            if len(parts) == 6:
                is_filesystem = check_if_sector_is_filesystem(file_path, parts[2])  # Use 'Start' as the sector offset
                sector_info = {
                    'Index': parts[0],
                    'Slot': parts[1],
                    'Start': parts[2],
                    'End': parts[3],
                    'Length': parts[4],
                    'Description': parts[5],
                    'IsFileSystem': is_filesystem
                }
                sectors_info.append(sector_info)
        print(sectors_info)
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
    
@app.route('/api/list-files', methods=['GET'])
def list_files():
    file_path = request.args.get('file_path', '')
    start_sector = request.args.get('start_sector', '')
    print("Info got")
    try:
        sector_offset = int(start_sector)
    except ValueError:
        return jsonify({'error': 'Invalid start_sector value'}), 400

    # Construct and run the 'fls' command
    cmd = ['fls', '-r', '-o', str(sector_offset), file_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to list files', 'details': str(e)}), 500

    # Function to parse the output from fls
    def parse_fls_output(fls_output):
        lines = fls_output.strip().split("\n")
        root = {"name": "root", "children": []}
        current_path = [root]  # This acts as our stack

        for line in lines:
            if not line.strip():
                continue
            
            parts = line.strip().split()
            # print(parts)
            deleted = '*' in parts
            if deleted:
                star_index = parts.index('*')
            else:
                star_index = -1
            # TODO: Consider * Deleted
            # Depending on whether the line starts with '+', adjust the index for type and inode
            # since there are two patterns
            # Pattern 1: Start with +
            # Pattern 2: Start with d/d or r/r which means it is at the root directory
            inode_index = 2 if star_index > 0 else 1
            name_index = 3 if star_index > 0 else 2

            entry_type = 'directory' if 'd/d' in parts[0] else 'file'
            inode = parts[inode_index].strip(':').strip('*')  # Remove any colons or asterisks from the inode field
            name = ' '.join(parts[name_index:]).strip(': "').strip('*')  # Clean up the name field
            # Added deleted for extra name process
            if deleted:
                name = name.split(' ')
                if len(name) > 1:
                    name = name[1]
                else:
                    name = name[0]
            while len(current_path) > 1:
                current_path.pop()

            parent_node = current_path[-1]
            new_node = {
                "name": name,
                "type": entry_type,
                "inode": inode,
                "deleted": deleted,
                "children": [] if entry_type == 'directory' else None
            }
            parent_node["children"].append(new_node)

            if entry_type == 'directory':
                current_path.append(new_node)
            # # Determine the level by counting the number of + at the start
            # level = parts[0].count('+') if parts[0].startswith('+') else 0

            # entry_type = 'directory' if 'd/d' in parts[0] else 'file'
            # print(inode)
            # inode = parts[inode_index].strip(':')
            # name = ' '.join(parts[name_index:]).strip(': "')

            # # Manage the stack according to the current level
            # while len(current_path) > level + 1:
            #     current_path.pop()

            # parent_node = current_path[-1]

            # # Create a new node
            # new_node = {
            #     "name": name,
            #     "type": entry_type,
            #     "inode": inode,
            #     "deleted": deleted,
            #     "children": [] if entry_type == 'directory' else None
            # }

            # # Append the new node to the parent's children
            # parent_node["children"].append(new_node)

            # # If it's a directory, push it onto the stack
            # if entry_type == 'directory':
            #     current_path.append(new_node)

        return root
    return jsonify(parse_fls_output(result.stdout))

if __name__ == '__main__':
    app.run(debug=True)
import shlex
import subprocess

def getFileBasics(file_name):
    # file_name = "/files/example.txt"
    command = f"cat {file_name}"

    # Use shlex to safely split the command string
    safe_command = shlex.split(command)

    # Execute the command using subprocess
    result = subprocess.run(safe_command, capture_output=True, text=True)

    # Check if the command was executed successfully
    if result.returncode == 0:
        print("File contents:")
        print(result.stdout)
        return result.stdout
    else:
        print("Error executing command:")
        print(result.stderr)

def get_file_md5_md5(file_path):
    command = f"md5 -q {file_path}"
    safe_command = shlex.split(command)
    result = subprocess.run(safe_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        # The output of `md5 -q` is just the hash
        md5_hash = result.stdout.strip()
        return md5_hash
    else:
        print("Error getting MD5 hash:", result.stderr)
        return None
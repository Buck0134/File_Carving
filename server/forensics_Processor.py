import hashlib
import shlex
import subprocess

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_contents(self):
        """Reads the file contents."""
        command = f"cat {self.file_path}"
        safe_command = shlex.split(command)
        result = subprocess.run(safe_command, capture_output=True, text=True)

        if result.returncode == 0:
            print("File contents:")
            print(result.stdout)
            return result.stdout
        else:
            print("Error executing command:")
            print(result.stderr)
            return None

    def get_file_md5(self):
        """Calculates the MD5 hash of the file using hashlib instead of an external command."""
        try:
            with open(self.file_path, 'rb') as file:
                file_bytes = file.read()  # Read the entire file
                md5_hash = hashlib.md5(file_bytes).hexdigest()
                return md5_hash
        except Exception as e:
            print(f"Error getting MD5 hash: {e}")
            return None
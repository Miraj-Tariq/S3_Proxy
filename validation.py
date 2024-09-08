import re

from dotenv import load_dotenv
import os

load_dotenv()

def validate_file(file):
    file_size = len(file.file.read())
    if file_size > int(os.getenv('MAX_FILE_SIZE_MB')) * 1024 * 1024:
        raise ValueError(f"File size exceeds {os.getenv('MAX_FILE_SIZE_MB')}MB limit")

    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{3,4}$', file.filename):
        raise ValueError("Invalid file name format")

    return True

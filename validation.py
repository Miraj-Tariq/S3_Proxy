import re
from pydantic import BaseModel, field_validator

# Allowed file extensions and max file size (e.g., 5MB)
ALLOWED_FILE_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE_MB = 50


def validate_bucket_name(bucket_name):
    if not (3 <= len(bucket_name) <= 63):
        raise ValueError('Bucket name length must be between 3 and 63 characters')
    if not re.match(r'^[a-z0-9.-]+$', bucket_name):
        raise ValueError('Bucket name must only contain lowercase letters, numbers, periods, or hyphens')
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', bucket_name):
        raise ValueError('Bucket name cannot be in IP address format')
    return bucket_name


def validate_object_name(object_name):
    if len(object_name) > 1024:
        raise ValueError('Object name cannot be more than 1024 characters long')
    return object_name



# File validation helper function
def validate_file(file):
    # Validate file size
    file_size = len(file.file.read())
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit")

    # # Reset file pointer to the start of the file
    # file.file.seek(0)
    #
    # # Validate file extension
    # file_extension = file.filename.split('.')[-1].lower()
    # if file_extension not in ALLOWED_FILE_EXTENSIONS:
    #     raise ValueError(f"Invalid file type. Allowed types: {', '.join(ALLOWED_FILE_EXTENSIONS)}")

    # Validate if file name is valid
    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{3,4}$', file.filename):
        raise ValueError("Invalid file name format")

    return True

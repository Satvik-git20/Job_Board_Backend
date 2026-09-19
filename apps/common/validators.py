import os
from django.core.exceptions import ValidationError

def validate_resume_file(value):
    """
    Validator to enforce:
    1. File extension is .pdf
    2. File size is <= 5MB (5 * 1024 * 1024 bytes)
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Only PDF files (.pdf) are allowed.')

    max_size_bytes = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size_bytes:
        raise ValidationError('File size exceeds the maximum limit of 5 MB.')

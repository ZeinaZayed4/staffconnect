from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ALLOWED_AVATAR_EXTENSION = ["jpg", "jpeg", "png"]
MAX_AVATAR_SIZE_MB = 2

validate_avatar_extension = FileExtensionValidator(allowed_extensions=ALLOWED_AVATAR_EXTENSION)

def validate_avatar_size(file):
    if file.size > MAX_AVATAR_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image is too large. The maximum size is {MAX_AVATAR_SIZE_MB} MB.")

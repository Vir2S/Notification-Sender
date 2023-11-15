from datetime import datetime
from django.core.exceptions import ValidationError


def validate_date(value):
    if value.timestamp() < datetime.now().timestamp():
        raise ValidationError("Date and time must be in the future, not in the past.")
    return value

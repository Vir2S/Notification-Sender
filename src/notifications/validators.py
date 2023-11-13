from datetime import datetime
from django.core.exceptions import ValidationError


def validate_date(value):
    if value.timestamp() < datetime.now().timestamp():
        raise ValidationError("Date must be future, not past.")
    return value

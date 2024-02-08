import random
import string

from .constants import DEFAULT_ID_LENGTH
from .models import URLMap


def is_unique_short_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return False
    return True


def get_short_id():
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    short_id = ''.join(random.choices(char_set, k=DEFAULT_ID_LENGTH))
    return short_id


def get_unique_short_id():
    short_id = get_short_id()
    while not is_unique_short_id(short_id):
        short_id = get_short_id()
    return short_id
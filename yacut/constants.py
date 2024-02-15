import string

DEFAULT_ID_LENGTH = 6
FORWARDING_VIEW_NAME = 'forwarding_view'

AUTO_SHORT_LENGTH = 6
GENERATE_SHORT_MAX_ATTEMPTS = 100
MAX_ORIGINAL_LENGTH = 2048
MAX_SHORT_LENGTH = 16
SHORT_LINK_VIEW = 'short_view'
REDIRECT_URL = 'forwarding_view'

CHARS = string.ascii_letters + string.digits
SHORT_REGEX = fr'^[{CHARS}]*$'
import re
from datetime import datetime
from random import choices

from flask import flash
from wtforms.validators import ValidationError

from yacut import db
from .constants import (
    CHARS,
    AUTO_SHORT_LENGTH,
    SHORT_REGEX, GENERATE_SHORT_MAX_ATTEMPTS,
    MAX_SHORT_LENGTH, MAX_ORIGINAL_LENGTH
)
from .handlers import InvalidAPIUsage, UnableToCreate

CAN_NOT_CREATE = 'Невозможно создать ID для короткой ссылки'
CUSTOM_ID_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
VALIDATION_ORIGINAL_ERROR = 'URL не может больше чем {}'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return db.session.query(URLMap).filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for attempt in range(GENERATE_SHORT_MAX_ATTEMPTS):
            short = ''.join(choices(CHARS, k=AUTO_SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise UnableToCreate(CAN_NOT_CREATE)

    @staticmethod
    def save(original, short, is_valid=False):
        if not (is_valid or len(original) <= MAX_ORIGINAL_LENGTH):
            raise ValidationError(
                VALIDATION_ORIGINAL_ERROR.format(MAX_ORIGINAL_LENGTH)
            )
        if not short:
            short = URLMap.get_unique_short_id()
            is_valid = True
        if not is_valid:
            if not (len(short) <= MAX_SHORT_LENGTH
                    and re.fullmatch(SHORT_REGEX, short)):
                raise ValidationError(INVALID_CUSTOM_ID)
            if URLMap.get(short):
                raise UnableToCreate(CUSTOM_ID_EXISTS)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return dict(
            original=self.original,
            short=self.short,
        )

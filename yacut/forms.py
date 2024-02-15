from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import SHORT_REGEX, MAX_SHORT_LENGTH, MAX_ORIGINAL_LENGTH


LONG_URL = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле.'
INVALID_URL = 'Некорректный URL'
YOUR_URL = 'Ваш вариант короткой ссылки'
ID_MUST_BE_SHORTER = 'Длина идентификатора должна быть не более 16 символов'
INVALID_FIELD = 'Указано недопустимое имя для короткой ссылки'
CREATE = 'Создать'
TOO_LONG_URL = 'Ваша ссылка слишком длинная'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_URL,
        validators=(
            DataRequired(message=REQUIRED_FIELD),
            URL(message=INVALID_URL),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message=TOO_LONG_URL
            )
        )
    )
    custom_id = StringField(
        YOUR_URL,
        validators=(
            Length(
                max=MAX_SHORT_LENGTH,
                message=ID_MUST_BE_SHORTER
            ),
            Optional(),
            Regexp(
                SHORT_REGEX,
                message=INVALID_FIELD
            ),
        )
    )
    submit = SubmitField(CREATE)

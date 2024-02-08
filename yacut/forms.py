from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import ID_PATTERN


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректный URL')
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(
                1, 16,
                message='Длина идентификатора должна быть не более 16 символов'
            ),
            Optional(),
            Regexp(
                ID_PATTERN,
                message='Указано недопустимое имя для короткой ссылки'
            ),
        )
    )
    submit = SubmitField('Создать')
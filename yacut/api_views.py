from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id):
    url_map_obj = URLMap.query.filter_by(short=short_id).first()
    if url_map_obj is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    response = {'url': url_map_obj.original}
    return jsonify(response), HTTPStatus.OK


@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    original = data['url']
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    short = data['custom_id']
    existing_url_map = URLMap.query.filter_by(short=short).first()
    if existing_url_map:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    try:
        url_map_obj = URLMap(original=original, short=short)
        url_map_obj.save()
    except ValueError:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    response = {
        'url': url_map_obj.original,
        'short_link': url_for(
            'forwarding_view',
            short=url_map_obj.short,
            _external=True
        )
    }

    return jsonify(response), HTTPStatus.CREATED
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import FORWARDING_VIEW_NAME
from .handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


ID_NOT_FOUND = 'Указанный id не найден'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_URL_FIELD = '\"url\" является обязательным полем!'
CUSTOM_ID_ALREADY_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'

@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id):
    url_map_links = URLMap.get_by_short(short_id)
    if url_map_links is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map_links.original}), HTTPStatus.OK



@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(MISSING_URL_FIELD)

    original = data['url']
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    short = data['custom_id']
    existing_url_map = URLMap.get_by_short(short)
    if existing_url_map:
        raise InvalidAPIUsage(CUSTOM_ID_ALREADY_EXISTS)

    try:
        url_map_obj = URLMap(original=original, short=short)
        url_map_obj.save()
    except ValueError:
        raise InvalidAPIUsage(INVALID_CUSTOM_ID)

    return jsonify({
        'url': url_map_obj.original,
        'short_link': url_for(
            FORWARDING_VIEW_NAME,
            short=url_map_obj.short,
            _external=True
        )
    }), HTTPStatus.CREATED

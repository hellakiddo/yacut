from http import HTTPStatus

from flask import jsonify, request, url_for
from wtforms import ValidationError

from . import app
from .constants import FORWARDING_VIEW_NAME
from .handlers import InvalidAPIUsage
from .models import URLMap


ID_NOT_FOUND = 'Указанный id не найден'
NO_REQUEST_BODY = 'Отсутствует тело запроса'
REQUIRED_FIELD = '"url" является обязательным полем!'

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
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if not data.get('url'):
        raise InvalidAPIUsage(REQUIRED_FIELD)
    short = data.get('custom_id')
    try:
        return jsonify(
            {
                'url': data['url'],
                'short_link': url_for(
                    FORWARDING_VIEW_NAME,
                    short=URLMap.save(
                        original=data['url'],
                        short=short,
                    ).short,
                    _external=True
                )}
        ), HTTPStatus.CREATED
    except ValidationError as error:
        raise InvalidAPIUsage(str(error))
from http import HTTPStatus

from flask import flash, redirect, render_template, url_for, abort

from . import app
from .constants import REDIRECT_URL, INDEX_HTML
from .forms import URLMapForm
from .handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_HTML, form=form)
    original = form.original_link.data
    short = form.custom_id.data
    try:
        return render_template(
            INDEX_HTML,
            form=form,
            short=url_for(
                endpoint=REDIRECT_URL,
                short=URLMap.save(
                    original=original, short=short, is_valid=False
                ).short,
                _external=True
            ))
    except (InvalidAPIUsage, ValueError) as error:
        flash(str(error))
    return render_template(INDEX_HTML, form=form)


@app.get('/<short>')
def forwarding_view(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)

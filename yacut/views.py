from http import HTTPStatus

from flask import flash, redirect, render_template, url_for, abort

from . import app
from .constants import FORWARDING_VIEW_NAME
from .forms import URLMapForm
from .handlers import UnableToCreate
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                endpoint=FORWARDING_VIEW_NAME,
                short=URLMap.save(
                    original=original, short=short, is_valid=False
                ).short,
                _external=True
            ))
    except (ValueError, UnableToCreate) as error:
        flash(str(error))
    return render_template('index.html', form=form)


@app.get('/<short>')
def forwarding_view(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)

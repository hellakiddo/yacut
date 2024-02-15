from http import HTTPStatus

from flask import flash, redirect, render_template, url_for, abort

from . import app
from .forms import URLMapForm
from .models import URLMap, CUSTOM_ID_EXISTS


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    try:
        if URLMap.get_by_short(short):
            flash(CUSTOM_ID_EXISTS)
            return render_template('exists_handler.html', form=form)
        return render_template(
            'index.html',
            form=form,
            context={
                'short': url_for(
                    endpoint='forwarding_view',
                    short=URLMap.save(
                        original=original, short=short, is_valid=True
                    ).short,
                    _external=True
                )})
    except Exception as error:
        flash(str(error))


@app.get('/<short>')
def forwarding_view(short):
    url_map = URLMap.get_by_short(short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
from flask import Flask
from flask import request, flash, redirect, url_for, render_template, send_file
from werkzeug.local import LocalProxy
import logging
import io
from app01.app01_model import AppModel
from flask import g

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

app = Flask(__name__, template_folder='static')

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['DEBUG'] = False
app.config['TESTING'] = False
try:
    app.config['SECRET_KEY'] = open('/app/app01/secret_key', 'rb').read()
except IOError as e:
    # use 'head -c 24 /dev/urandom > secret_key' to create a key
    # raise e
    logging.warning("SECRET_KEY was not generated. Use 'head -c 24 /dev/urandom > /app/app01/secret_key' to create a key")
    app.config['SECRET_KEY'] = 'some_secret'

try:
    app.config.from_envvar('NNAPP_SETTINGS_PATH')
except (RuntimeError, FileNotFoundError) as e:
    logging.warning("NNAPP_SETTINGS_PATH was not set. Use 'export NNAPP_SETTINGS_PATH=\"/app/app01/config.cfg\"'")


def get_model():
    _model = getattr(g, 'app_model', None)
    if _model is None:
        _model = g.app_model = AppModel()
        g.app_model.load_resources()
    return _model


model = LocalProxy(get_model)


@app.route('/', methods=['GET'])
def index():
    return render_template('index_t.html')


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('File name is empty')
        return redirect(url_for('index'))

    try:
        if file:
            str_in = file.read()
            file.close()

            res = get_model().replace(str_in.decode('utf-8'))
            str_out = io.BytesIO()
            str_out.write(res.encode('utf-8'))
            str_out.seek(0)

            return send_file(str_out, attachment_filename=file.filename, as_attachment=True, mimetype='text/csv')
    except RuntimeError:
        flash('Something bad happened')
    return redirect(url_for('index'))
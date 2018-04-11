"""
WEB View implementation with Flash Framework.
Page View is created with Upload form.
Root(/) end point serve index page and form Upload function
API endpoints: /api/convert, api/callcounter
Supplementary endpoint: /raw/convert
"""

from flask import Flask
from flask import request, flash, redirect, url_for, render_template, send_file, jsonify, make_response, abort
import logging
import io
from functools import wraps
from app01.app01_model import AppModel

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

model = None
app = Flask(__name__, template_folder='static')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DEBUG'] = False
app.config['TESTING'] = False

try:
    app.config['SECRET_KEY'] = open('/app/app01/secret_key', 'rb').read()
except IOError as e:
    logging.warning(
        "SECRET_KEY was not generated. Use 'head -c 24 /dev/urandom > /app/app01/secret_key' to create a key"
    )
    app.config['SECRET_KEY'] = 'some_secret'

try:
    app.config.from_envvar('NNAPP_SETTINGS_PATH')
except (RuntimeError, FileNotFoundError) as e:
    logging.warning("NNAPP_SETTINGS_PATH was not set. Use 'export NNAPP_SETTINGS_PATH=\"/app/app01/config.cfg\"'")


def limit_content_length(max_length):
    """
    Annotator rejects all invocation with content larger than max_length
    :param max_length: max content size
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def get_model():
    """
    Factory method for Model singleton object
    :return: application model object
    """
    global model
    if model is None:
        model = AppModel()
        model.load_resources()
    return model


@app.route('/', methods=['GET'])
def index():
    """
    Serves root HTML page
    Renders static page from a template with variables
    """
    return render_template(
        'index_t.html',
        call_counter=str(get_model().call_counter),
        app_version=str(app.config.get('GIT_HASH', None))
    )


@app.route('/', methods=['POST'])
@limit_content_length(app.config['MAX_CONTENT_LENGTH'])
def upload_file():
    """
    Serves HTML upload form
    Request arrives with content-type: multipart/form-data
    Target file saved into 'files' dictionary, with key 'file'
    """
    try:
        if 'file' not in request.files:
            flash("No file selected or file is too big (max size is %sB)" % app.config['MAX_CONTENT_LENGTH'])
            return redirect(url_for('index'))

        file = request.files['file']
        str_in = file.read()
        file.close()

        str_out = io.BytesIO()
        str_out.write(process_text(str_in.decode('utf-8')).encode('utf-8'))
        str_out.seek(0)

        return send_file(
            str_out,
            attachment_filename=file.filename,
            as_attachment=True,
            mimetype='text/plain'
        )
    except RuntimeError:
        flash('Something bad happened')
    return redirect(url_for('index'))


@app.route('/raw/convert', methods=['POST'])
@limit_content_length(app.config['MAX_CONTENT_LENGTH'])
def raw_convert_file():
    """
    Serves handy endpoint
    Convert raw input data, returns converted raw text
    Method : POST
    Data Params : [bytes]
    Response Codes: Success (200 OK), Bad Request (400)
    Response Data: [bytes]
    """
    try:
        str_out = io.BytesIO()
        str_out.write(process_text(request.data.decode('utf-8')).encode('utf-8'))
        str_out.seek(0)

        return send_file(
            str_out,
            attachment_filename='result.txt',
            as_attachment=True,
            mimetype='text/plain'
        )
    except:
        return make_response('', 400)


@app.route('/api/convert', methods=['POST'])
@limit_content_length(app.config['MAX_CONTENT_LENGTH'])
def api_convert():
    """
    Serves RESTFULL Convert endpoint
    Method : POST
    Data Params : { text : [string]}
    Response Codes: Success (200 OK), Bad Request (400)
    Response Data: { text : [string]} | { error : [string]}
    """
    try:
        rest_data = request.get_json()
        text = rest_data.get('text')
        return jsonify({'text': process_text(text)})
    except Exception as e:
        response = jsonify({'error': 'API error'})
        response.status_code = 400
        return response


@app.route('/api/callcounter', methods=['GET'])
def api_callcounter():
    """
    Serves RESTFULL call counter endpoint
    Method : GET
    Response Codes: Success (200 OK), Bad Request (400)
    Response Data: { callcounter : [integer]} | { error : [string]}
    """
    try:
        return jsonify({'callcounter': get_model().call_counter})
    except Exception as e:
        response = jsonify({'error': 'API error'})
        response.status_code = 400
        return response


def process_text(str_in):
    """
    Atomic call to convert text and increment call counter
    :param str_in: string to convert
    :return: converted string
    """
    str_out = get_model().replace(str_in)
    get_model().inc_call_counter()
    return str_out

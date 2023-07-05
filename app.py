from dbhelpers import run_statement
from dbcreds import production_mode
from apihelpers import check_data, save_file
from flask import Flask, request, make_response, jsonify, send_from_directory
import uuid
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000000

@app.post('/api/user')
def post_user():
    error = check_data(request.form, ['email', 'username', 'password'])
    if(error != None):
        return make_response(jsonify(error), 400)
    error = check_data(request.files, ['image'])
    if(error != None):
        return make_response(jsonify(error), 400)
    if(request.content_length < (0.5 * 1000000)):
        filename = save_file(request.files['image'])
    if(filename == None):
        return make_response(jsonify("Something has gone wrong"), 500)
    token = uuid.uuid4().hex
    salt = uuid.uuid4().hex
    results = run_statement('call post_user(?,?,?,?,?,?,?)', [request.form.get('email'), request.form.get('username'), filename, request.form.get('bio'), request.form.get('password'), token, salt])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Something went wrong", 500)


if(production_mode == True):
    print('Running in production mode')
    import bjoern # type: ignore
    bjoern.run(app, '0.0.0.0', 5000)
else:
    print('Running in development mode')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
    CORS(app)

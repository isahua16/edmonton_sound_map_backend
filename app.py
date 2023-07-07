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
        filename = save_file(request.files['image'], 'images', ['gif','png','jpg','jpeg', 'webp'])
    if(filename == None):
        return make_response(jsonify("Something has gone wrong"), 500)
    token = uuid.uuid4().hex
    salt = uuid.uuid4().hex
    results = run_statement('call post_user(?,?,?,?,?,?,?)', [request.form.get('email'), request.form.get('username'), filename, request.form.get('bio'), request.form.get('password'), token, salt])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Something went wrong", 500)

@app.post('/api/login')
def post_login():
    error = check_data(request.json, ['email', 'password'])
    if(error != None):
        return make_response(jsonify(error), 400)
    token = uuid.uuid4().hex
    results = run_statement('call post_login(?,?,?)', [request.json.get('email'), request.json.get('password'), token])
    if(type(results) == list and results != []):
        return make_response(jsonify(results), 200)
    elif(type(results) == list and results == []):
        return make_response(jsonify("Invalid password or email"), 400)
    else:
        return make_response('Something went wrong', 500)
    
@app.post('/api/feature')
def post_feature():
    error = check_data(request.form, ['lat', 'long', 'location', 'name', 'description', 'is_interior', 'is_mechanical', 'is_natural', 'is_societal', 'season', 'time', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    error = check_data(request.files, ['audio'])
    if(error != None):
        return make_response(jsonify(error), 400)
    audio_file = save_file(request.files['audio'], 'audio', ['wav','mp4','mp3'])
    feature_image = None
    if(request.files.get('image') != None):
        feature_image = save_file(request.files['image'], 'images', ['gif','png','jpg','jpeg','webp'])
    if(audio_file == None):
        return make_response(jsonify("Something has gone wrong"), 500)
    results = run_statement('call post_feature(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [request.form.get('lat'), request.form.get('long'), feature_image, request.form.get('location'), request.form.get('name'), request.form.get('description'), request.form.get('is_interior'), request.form.get('is_mechanical'), request.form.get('is_natural'), request.form.get('is_societal'), request.form.get('season'), request.form.get('time'), request.form.get('token'), audio_file])
    if(type(results) == list and results != []):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.get('/api/features')
def get_features():
    results = run_statement('call get_features()')
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.get('/api/feature/image')
def get_feature_image():
    error = check_data(request.args, ['feature_id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_feature_image(?)', [request.args.get('feature_id')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Feature doesn't exist"), 400)
    feature_image = send_from_directory('images', results[0]['feature_image'])
    return feature_image

@app.get('/api/user/image')
def get_user_image():
    error = check_data(request.args, ['feature_id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_user_image(?)', [request.args.get('feature_id')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Feature doesn't exist"), 400)
    feature_image = send_from_directory('images', results[0]['user_image'])
    return feature_image

@app.get('/api/feature/audio')
def get_feature_audio():
    error = check_data(request.args, ['feature_id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_feature_audio(?)', [request.args.get('feature_id')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Feature doesn't exist"), 400)
    feature_audio = send_from_directory('audio', results[0]['feature_audio'])
    return feature_audio

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

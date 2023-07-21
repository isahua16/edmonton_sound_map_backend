from dbhelpers import run_statement
from dbcreds import production_mode
from apihelpers import check_data, save_file, delete_file
from flask import Flask, request, make_response, jsonify, send_from_directory
import uuid
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000000

@app.post('/api/user')
def post_user():
    error = check_data(request.json, ['email', 'username', 'password'])
    if(error != None):
        return make_response(jsonify(error), 400)
    token = uuid.uuid4().hex
    salt = uuid.uuid4().hex
    results = run_statement('call post_user(?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('username'), request.json.get('image'), request.json.get('bio'), request.json.get('password'), token, salt])
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
    if(request.form.get('is_interior') == 0 and request.form.get('is_mechanical') == 0 and request.form.get('is_natural') == 0 and request.form.get('is_societal') == 0):
        return make_response("Feature must contain at least one category", 400) 
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

@app.patch('/api/admin/feature')
def patch_any_feature_info():
    results = run_statement('call patch_any_feature_info(?,?,?,?,?,?,?,?,?,?)', [request.json.get('token'), request.json.get('feature_id'), request.json.get('name'), request.json.get('description'), request.json.get('is_interior'), request.json.get('is_mechanical'),request.json.get('is_natural'), request.json.get('is_societal'), request.json.get('season'),request.json.get('time')])
    if(type(results) == list):
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

@app.get('/api/admin/feature/image')
def get_new_feature_image():
    error = check_data(request.args, ['feature_id', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_new_feature_image(?,?)', [request.args.get('token'), request.args.get('feature_id')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Feature doesn't exist"), 400)
    feature_image = send_from_directory('images', results[0]['feature_image'])
    return feature_image

@app.patch('/api/admin/feature/image')
def patch_any_feature_image():
    error = check_data(request.form, ['token', 'feature_id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    error = check_data(request.files, ['image'])    
    if(error != None):
        return make_response(jsonify(error), 400)
    old_results = run_statement('call get_feature_image(?)', [request.form.get('feature_id')])
    if(type(old_results) == list):
        new_image = save_file(request.files['image'], 'images', ['gif','png','jpg','jpeg','webp'])
        new_results = run_statement('call patch_any_feature_image(?,?,?)', [request.form.get('token'),request.form.get('feature_id'), new_image])
        if(type(new_results) == list and new_results[0]['updated_rows'] == 1):
            if (old_results[0]['user_image'] != 'c1c831b2-7542-459b-8f94-6e639e1bacb2.jpg'):
                delete_file(old_results[0]['user_image'], 'images')
            return make_response(jsonify(new_results), 200)
        else:
            return make_response('Something went wrong', 500)  
    else:
        return make_response('Something went wrong', 500)

@app.get('/api/user/image')
def get_user_image():
    error = check_data(request.args, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_user_image(?)', [request.args.get('token')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("User doesn't exist"), 400)
    user_image = send_from_directory('images', results[0]['user_image'])
    return user_image

@app.patch('/api/user/image')
def patch_user_image():
    error = check_data(request.form, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    error = check_data(request.files, ['image'])    
    if(error != None):
        return make_response(jsonify(error), 400)
    old_image_results = run_statement('call get_user_image(?)', [request.form.get('token')])
    if(type(old_image_results) == list):
        new_image = save_file(request.files['image'], 'images', ['gif','png','jpg','jpeg','webp'])
        new_image_results = run_statement('call patch_user_image(?,?)', [new_image, request.form.get('token')])
        if(type(new_image_results) == list and new_image_results[0]['updated_rows'] == 1):
            if (old_image_results[0]['user_image'] != 'f46d31d3-e1ec-4023-8978-9674af319155.jpg'):
                delete_file(old_image_results[0]['user_image'], 'images')
            return make_response(jsonify(new_image_results), 200)
        else:
            return make_response('Something went wrong', 500)  
    else:
        return make_response('Something went wrong', 500)
    
@app.get('/api/user')
def get_user():
    error = check_data(request.args, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_user_profile(?)', [request.args.get('token')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

@app.patch('/api/user')
def patch_user():
    results = run_statement('call patch_user_info(?,?,?,?)', [request.json.get("token"), request.json.get('email'), request.json.get('username'), request.json.get('bio')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.delete('/api/user')
def delete_user():
    error = check_data(request.json, ['password', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call delete_user(?,?)', [request.json.get('password'), request.json.get('  ')])
    if(type(results) == list and results[0]['deleted_rows'] == 1):
        return make_response(jsonify(results), 200)
    elif(type(results) == list and results[0]['deleted_rows'] == 0):
        return make_response(jsonify(results), 400)
    else:
        return make_response('Something went wrong', 500)

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

@app.get('/api/admin/feature/audio')
def get_new_feature_audio():
    error = check_data(request.args, ['feature_id', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_new_feature_audio(?,?)', [request.args.get('token'), request.args.get('feature_id')])
    if(type(results) != list):
        return make_response(jsonify(results), 500)
    elif(len(results) == 0):
        return make_response(jsonify("Feature doesn't exist"), 400)
    feature_audio = send_from_directory('audio', results[0]['feature_audio'])
    return feature_audio

@app.delete('/api/login')
def delete_function():
    error = check_data(request.json, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call delete_login(?)', [request.json.get('token')])
    if(type(results) == list and results[0]["deleted_rows"] == 1 ):
        return make_response(jsonify(results), 200)
    elif(type(results) == list and results[0]["deleted_rows"] == 0 ):
        return make_response(jsonify(results), 400)
    else:
        return make_response('Something went wrong', 500)
    
@app.get('/api/admin/features')
def get_all_features():
    error = check_data(request.args, ['token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call get_new_features(?)', [request.args.get('token')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.patch('/api/admin/feature/approve')
def approve_feature():
    error = check_data(request.json, ['feature_id', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call approve_feature(?,?)', [request.json.get('token'), request.json.get('feature_id')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.patch('/api/admin/feature/reject')
def reject_feature():
    error = check_data(request.json, ['feature_id', 'token'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call reject_feature(?,?)', [request.json.get('token'), request.json.get('feature_id')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)
    
@app.delete('/api/admin/feature')
def delete_feature():
    error = check_data(request.json, ['token', 'feature_id'])
    if(error != None):
        return make_response(jsonify(error), 400)
    results = run_statement('call delete_any_feature(?,?)', [request.json.get('token'), request.json.get('feature_id')])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response('Something went wrong', 500)

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

from dbhelpers import run_statement
from dbcreds import production_mode
from apihelpers import check_data, save_file
from flask import Flask, request, make_response, jsonify, send_from_directory
import uuid
app = Flask(__name__)
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

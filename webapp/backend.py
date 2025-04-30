# app.py
from flask import Flask, request, jsonify, Response
import flask_cors 
from flask_cors import CORS



app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500"])

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/my-function', methods=['POST'])
@flask_cors.cross_origin(origin='http://localhost:5500')
def my_function():
    data = request.get_json()
    result = f"Hello, {data['name']}!"  # Your logic here
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)

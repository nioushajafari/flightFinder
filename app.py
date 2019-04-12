from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import flights
import os
app = Flask(__name__)
# Enable Cross-Origin-Requests since Create-React-App is served locally on a different port. In the future this won't be neccessary once everything is served from one webserver.
CORS(app)

@app.route('/search', methods=['POST'])
def hello_does_naming_this_do_anything():
    params = request.get_json()
    return jsonify(flights.doSomething(params))

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)

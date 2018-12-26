from flask import Flask, Response

app = Flask(__name__)

@app.route('/ping')
def ping_response():
    return Response('ErrorRate: 2.35\nActiveUsers: 531\n',
            mimetype='text/plain')

from flask import Flask, Response

app = Flask(__name__)

@app.route('/ping')
def ping_response():
    return Response('ErrorRate: 2.35\nActiveUsers: 531\n',
            mimetype='text/plain')

@app.route('/ping-bad-response')
def ping_bad_response():
    return Response('ErrorRate: NULL\n',
            mimetype='text/plain')

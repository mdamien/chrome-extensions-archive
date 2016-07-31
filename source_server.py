# some simple service to execute a regex search on the extension sources

import flask
from flask import request
import subprocess
import time

app = flask.Flask(__name__)

@app.route('/')
def index():
    q = request.args.get('q')
    def inner():
        proc = subprocess.Popen(
            ['ag', str(q), 'crawled/sources/'],
            stdout=subprocess.PIPE
        )
        for line in iter(proc.stdout.readline, ''):
            yield line.rstrip().decode('utf8')+'\n'

    return flask.Response(inner(), mimetype='text/text')

app.run(debug=True, port=5000)

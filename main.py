from flask import Flask, render_template, jsonify, request, Response, stream_with_context
import json

# https://www.html5rocks.com/en/tutorials/eventsource/basics/
# https://web.dev/fetch-upload-streaming/

web_site = Flask(__name__)
import csv
import time

def generator():
  csvfile = csv.DictReader(open('movies.csv'))
  count = 0
  for row in csvfile:
      time.sleep(1.0)
      count = count + 1
      yield 'id:'+str(count)+'\ndata: '+json.dumps(row)+'\n\n'
  yield 'data: done\n\n'

@web_site.route('/')
def index():
  return render_template('index.html')

# file stream prompts download
@web_site.route('/movies/file')
def movie_stream():
  return Response(stream_with_context(generator()), mimetype='text/csv')

# event stream buffers data
@web_site.route('/movies/stream')
def movie_event():
  return Response(stream_with_context(generator()), mimetype="text/event-stream")

web_site.run(host='0.0.0.0', port=8080, debug=True)
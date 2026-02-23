import os
import urllib.request
import urllib.error
from flask import Flask, request, Response, send_file
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('wallet-tracker.html')

@app.route('/proxy')
def proxy():
    target = unquote(request.query_string.decode('utf-8'))
    if not target.startswith('https://'):
        return {'error': 'invalid target'}, 400

    try:
        req = urllib.request.Request(target, headers={
            'User-Agent':      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer':         'https://gmgn.ai/',
            'Accept':          'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            content_type = r.headers.get('Content-Type', 'application/json')

        return Response(data, status=200, content_type=content_type,
                        headers={'Access-Control-Allow-Origin': '*'})

    except urllib.error.HTTPError as e:
        body = e.read()
        return Response(body, status=e.code, content_type='application/json',
                        headers={'Access-Control-Allow-Origin': '*'})
    except Exception as e:
        return {'error': str(e)}, 502

@app.route('/proxy', methods=['OPTIONS'])
def proxy_options():
    return Response('', headers={
        'Access-Control-Allow-Origin':  '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': '*',
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

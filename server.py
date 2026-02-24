import os
import cloudscraper
from flask import Flask, request, Response, send_file
from urllib.parse import unquote

app = Flask(__name__)

# cloudscraper mimics a real browser and bypasses Cloudflare protection
# This is what lets us fetch wallet stats for any address, not just leaderboard ones
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

@app.route('/')
def index():
    return send_file('wallet-tracker.html')

@app.route('/proxy')
def proxy():
    target = unquote(request.query_string.decode('utf-8'))
    if not target.startswith('https://'):
        return {'error': 'invalid target'}, 400

    try:
        r = scraper.get(target, timeout=15, headers={
            'Referer':         'https://gmgn.ai/',
            'Accept':          'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        return Response(
            r.content, status=r.status_code,
            content_type=r.headers.get('Content-Type', 'application/json'),
            headers={'Access-Control-Allow-Origin': '*'}
        )
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

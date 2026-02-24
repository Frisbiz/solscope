import os
import json
import cloudscraper
from flask import Flask, request, Response, send_file
from urllib.parse import unquote

app = Flask(__name__)

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

HEADERS = {
    'Referer':         'https://gmgn.ai/',
    'Accept':          'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
}

@app.route('/')
def index():
    return send_file('wallet-tracker.html')

@app.route('/proxy')
def proxy():
    target = unquote(request.query_string.decode('utf-8'))
    if not target.startswith('https://'):
        return {'error': 'invalid target'}, 400
    try:
        r = scraper.get(target, timeout=15, headers=HEADERS)
        return Response(
            r.content, status=r.status_code,
            content_type=r.headers.get('Content-Type', 'application/json'),
            headers={'Access-Control-Allow-Origin': '*'}
        )
    except Exception as e:
        return Response(
            json.dumps({'error': str(e)}), status=502,
            content_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )

# Debug endpoint: hit multiple known wallet stat URLs and return all raw responses
# Usage: /debug?addr=8y83ZUQH8gsbYa9qEyYF6Wdqw3so7L9ThsWREuCVXWTr
@app.route('/debug')
def debug():
    addr = request.args.get('addr', '')
    if not addr:
        return {'error': 'pass ?addr=WALLET_ADDRESS'}, 400

    endpoints = {
        'walletNew_7d':  f'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{addr}?period=7d',
        'walletNew_30d': f'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{addr}?period=30d',
        'wallet_stat_7d':  f'https://gmgn.ai/defi/quotation/v1/wallet_stat/sol/{addr}?period=7d',
        'wallet_stat_30d': f'https://gmgn.ai/defi/quotation/v1/wallet_stat/sol/{addr}?period=30d',
        'analysis_30d':  f'https://gmgn.ai/api/v1/wallet_analysis/sol/{addr}?period=30d',
        'analysis_7d':   f'https://gmgn.ai/api/v1/wallet_analysis/sol/{addr}?period=7d',
        'activity':      f'https://gmgn.ai/defi/quotation/v1/wallet_activity/sol/{addr}?limit=1',
    }

    results = {}
    for name, url in endpoints.items():
        try:
            r = scraper.get(url, timeout=10, headers=HEADERS)
            try:
                results[name] = {'status': r.status_code, 'data': r.json()}
            except Exception:
                results[name] = {'status': r.status_code, 'raw': r.text[:500]}
        except Exception as e:
            results[name] = {'error': str(e)}

    return Response(
        json.dumps(results, indent=2),
        content_type='application/json',
        headers={'Access-Control-Allow-Origin': '*'}
    )

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

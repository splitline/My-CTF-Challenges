from bottle import default_app, get, run, request, response, template

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

from configs import secret

app = default_app()


@get("/")
def home():
    session = request.get_cookie('session', secret=secret)
    if not session:
        session = {"payloads": []}
        response.set_cookie('session', session, secret=secret)
    return template('index', payloads=session['payloads'])


@get("/proxy")
def proxy():
    url = request.params.url

    sess = request.get_cookie('session', secret=secret)
    sess['payloads'].append(url)
    response.set_cookie('session', sess, secret=secret)

    netloc = urlparse(url).netloc.lower()

    if netloc == '':
        response.status = 400
        response.content_type = 'text/plain'
        return "400: urlparse(url).netloc should not be empty"

    if netloc in ('localhost', '127.0.0.1', '127.0.1', '127.1', '2130706433', '0x7f000001'):
        response.status = 400
        response.content_type = 'text/plain'
        return "400: netloc should not be localhost, don't SSRF me!"

    try:
        resp = urlopen(url)
        response.content_type = resp.info().get_content_type()
        return resp.read()
    except (URLError, HTTPError) as e:
        response.status = 500
        return f"Fetch `{url}` failed: {e.reason}"


if __name__ == '__main__':
    run(host='localhost', port=9453, reloader=True)

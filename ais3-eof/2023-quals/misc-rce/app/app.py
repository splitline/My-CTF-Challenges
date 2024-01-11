from flask import Flask, request, send_file

import multiprocessing
import os

app = Flask(__name__)


def run(code):
    os.setgid(65534)
    os.setuid(65534)

    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()) as f:
        exec(code, {})
    return f.getvalue()


@app.route('/')
def index():
    return send_file('index.html')


@app.post('/exec')
def do_exec():
    code = request.json.get('code', '')
    p = multiprocessing.Pool(processes=1)
    result = p.apply_async(run, (code,))
    try:
        return str(result.get(timeout=1)), 200
    except multiprocessing.TimeoutError:
        p.terminate()
        return 'err: timeout', 500
    except Exception as e:
        return f"err: {e}", 500


if __name__ == '__main__':
    app.run()

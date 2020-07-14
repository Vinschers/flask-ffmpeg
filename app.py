import os
import subprocess
from flask import Flask, request
import ffmpeg
import tempfile
import shlex


def process(in_file, out_file):
    cmd = 'ffmpeg -f matroska -i pipe:0 -vcodec libx265 -f matroska pipe:1'
    p = subprocess.Popen(shlex.split(cmd), stdin=in_file, stdout=out_file)
    p.wait()


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    up_file = request.files['file'].stream

    in_file = tempfile.TemporaryFile()
    in_file.write(up_file.read())
    in_file.seek(0)
    out_file = tempfile.TemporaryFile()

    process(in_file, out_file)

    out_file.seek(0)

    return out_file.read()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

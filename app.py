import os
import subprocess
from flask import Flask, request, Response
import ffmpeg
import tempfile
import shlex
import threading
import io

class VideoConverter(object):
    def __init__(self, bytes):
        self.input = io.BytesIO(bytes)

    def _execute_process(self, p:subprocess.Popen, read_chunk_size=-1):
        def getData(p):
            while True:
                chunk = self.input.read(read_chunk_size)
                if not chunk:
                    break
                p.stdin.write(chunk)

            p.stdin.close()
            self.input.seek(0)

        def sendData(p):
            out = p.stdout
            while True:
                try:
                    chunk = out.read(8*1024)
                    if not chunk:
                        raise Exception()
                    yield chunk
                except Exception:
                    out.close()
                    p.wait()
                    break

        tGet = threading.Thread(target=getData, args=(p,))
        tGet.start()

        for c in sendData(p):
            yield c

    def custom_process(self, read_chunk_size=-1):
        p = (
            ffmpeg
            .input('pipe:', format='matroska')
            .output('pipe:', vcodec='libx265', format='matroska')
            .overwrite_output()
            .run_async(pipe_stdin=True, pipe_stdout=True)
        )
        
        for chunk in self._execute_process(p):
            yield chunk


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    conv = VideoConverter(file.read())

    return Response(conv.custom_process())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

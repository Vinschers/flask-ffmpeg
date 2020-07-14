import requests


with requests.post('http://localhost:5000/upload',
                   files={'file': ('', open(input("file: "), 'rb'))},
                   stream=True) as r:
    r.raise_for_status()
    with open('output.mkv', 'wb') as f:
        for chunk in r.iter_content(1024*3):
            f.write(chunk)
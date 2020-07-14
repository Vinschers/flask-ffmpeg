import requests


with requests.post('http://localhost:5000/upload',
                   files={'file': ('', open(input("file: "), 'rb'))}) as r:
    r.raise_for_status()
    with open('output.mkv', 'wb') as f:
        f.write(r.content)
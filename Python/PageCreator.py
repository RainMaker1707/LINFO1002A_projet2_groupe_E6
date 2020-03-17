from flask import Flask

app = Flask(__name__)


@app.route('/')
def test():
    return '<html><title>AAAA</title></html>'


print(test())

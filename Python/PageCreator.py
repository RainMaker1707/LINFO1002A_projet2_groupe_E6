import Python.PageReader as Page
from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    content_str = Page.read_file("./Html/home.html")
    return content_str


print(home())

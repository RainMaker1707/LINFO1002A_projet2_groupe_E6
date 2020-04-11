from flask import Flask, render_template, url_for
app = Flask(__name__, template_folder='templates', static_folder='style')


@app.route('/')
def home():
    """
    :return:
    """
    return render_template("base.html", STYLE=url_for('static', filename="base.css"))

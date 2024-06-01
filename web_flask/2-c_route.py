#!/usr/bin/python3
"""
This is the hello route module
Written by: Alemi Herbert 2024
"""


from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """
    This is the main route of the application
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    This is yet another route
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """
    This is yet another route, but with special text handling
    """
    return text.replace('_', ' ')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")

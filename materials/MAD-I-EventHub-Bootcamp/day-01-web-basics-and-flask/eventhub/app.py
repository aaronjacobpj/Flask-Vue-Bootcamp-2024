"""EventHub - Day 1: your first Flask app.

Run:  python app.py   then open http://127.0.0.1:5000
"""
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    # A view function returns the response body. For now, plain HTML in a string.
    return """
        <h1>EventHub</h1>
        <p>Book seats for events near you.</p>
        <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/hello/Aaron">Say hello</a></li>
            <li><a href="/hello/Aaron?times=3">Say hello 3 times</a></li>
            <li><a href="/request-info">See your request</a></li>
        </ul>
    """


@app.route("/about")
def about():
    return "<h1>About</h1><p>EventHub is the MAD I bootcamp demo app.</p>"


@app.route("/hello/<name>")
def hello(name):
    # <name> is a *path variable*: /hello/Priya -> name = "Priya"
    # ?times=3 is a *query string*: read it from request.args
    times = request.args.get("times", default=1, type=int)
    return "<br>".join(f"Hello, {name}!" for _ in range(times))


@app.route("/request-info")
def request_info():
    # Everything the browser sent us is inside the `request` object.
    return {
        "method": request.method,
        "path": request.path,
        "query_string": request.args.to_dict(),
        "user_agent": request.headers.get("User-Agent"),
    }  # returning a dict -> Flask sends JSON


if __name__ == "__main__":
    # debug=True: auto-reload on save + detailed error pages. Never use in production.
    app.run(debug=True)

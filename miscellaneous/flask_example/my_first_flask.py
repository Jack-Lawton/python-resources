
# Flask imports
import flask
from flask import request, jsonify

# Cross-Origin Resource Sharing
# This is magic to let us more easily call Flask from different test scripts/environments
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route('/')
def index():
    my_response = {
        "text": "Hello World"
    }
    return jsonify(my_response)


@app.route('/website')
def website():
    return """
    <h1>Look!</h1>
    <h2>What is it?</h2>
    <div style="display: flex; justify-content: flex-end">
      <div>I can use HTML formatting too!<p/>Isn't that cool?</div>
    </div>
    <h2>I guess so...</h2>
    """


@app.route('/post_request', methods=['POST'])
def post_request():
    payload = request.get_json(force=True)
    return jsonify({"payload": str(payload)})


@app.route('/params')
def params():
    my_parameter = request.args.get("my_parameter")
    return jsonify({"my_parameter": my_parameter})


@app.route('/dynamic/<x>')
def dynamic_url(x):
    return jsonify({"text": "You tried to access {}!".format(x)})


if __name__ == "__main__":
    app.run(port=5000)



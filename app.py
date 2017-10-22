from flask import Flask, jsonify, make_response, abort
import re

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/api/email/<email>/validate", methods=["GET"])
def validate_email(email):
    # general email regex (RFC 5322 official standard)
    # modified to separate username and email domain
    validator = re.compile("(^[a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    match_res = validator.match(email)

    if (match_res):
        print match_res.groups()
    else:
        abort(500)


    return make_response("Ok", 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(debug=True)

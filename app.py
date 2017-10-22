from flask import Flask, jsonify, make_response, abort
from dns import resolver
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
        BAD_DNS = "92.242.140.20"
        dns = match_res.groups()[1]
        answers = resolver.query(dns)
        for answer in answers:
            abort(500) if answer.to_text() == BAD_DNS else None
    else:
        abort(500)

    return make_response(jsonify({"success": True}), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(debug=True)

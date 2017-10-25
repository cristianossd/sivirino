import re
import socket
import smtplib as smtp
from flask import Flask, jsonify, make_response, abort
from dns import resolver

app = Flask(__name__)

@app.route("/api/email/<email>/validate", methods=["GET"])
def validate_email(email):
    # general email regex (RFC 5322 official standard)
    # modified to separate username and email domain
    validator = re.compile("(^[a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    match_res = validator.match(email)

    if (match_res):
        user, dns = match_res.groups()
        try:
            answers = resolver.query(dns, 'MX')
        except:
            abort(500)

        host = socket.gethostname()

        record = str(answers[0].exchange)
        server = smtp.SMTP()
        server.set_debuglevel(0)

        server.connect(record)
        server.helo(host)
        server.mail(email)
        code, message = server.rcpt(email)
        server.quit()

        abort(500) if code != 250 else None
    else:
        abort(500)

    return make_response(jsonify({"success": True}), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)

if __name__ == "__main__":
    app.run(debug=True)

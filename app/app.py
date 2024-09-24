from flask import Flask, jsonify
from werkzeug import exceptions

app = Flask(__name__)
ctx = app.app_context()

class HttpMethod():
    GET = "GET"

@app.route('/getcode', methods=[HttpMethod.GET])
def get_code():
    res = 'Random number or message test merge'
    return jsonify(res)

@app.route('/plus/<num1>/<num2>', methods=[HttpMethod.GET])
def plus(num1, num2):
    try:
        cal = float(num1) + float(num2)
        
        if (cal.is_integer()):
            cal = int(cal)

    except Exception as err:
        raise exceptions.BadRequest(err)

    return jsonify(cal)

if __name__ == '__main__':
    app.run(debug=True)
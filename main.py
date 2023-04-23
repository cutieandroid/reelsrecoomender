from flask import Flask, jsonify,request
from recommender import recommend

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/sumit/<string:id>")
def sum(id):
    result={
        "reelid":id,
        "source":"https://cdnfuirestore",
        "description":"jinglal hue hue"

    }

    return jsonify(result)

@app.route('/recommends/<string:shortcode>')
def predict(shortcode):
    prediction=recommend(shortcode)
    return jsonify(prediction)

@app.after_request
def after_request(response):
    white_origin= ['http://localhost:3000','http://localhost:3001']
    if request.headers['Origin'] in white_origin:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    return response




if(__name__=='__main__'):
    app.run(debug=True)

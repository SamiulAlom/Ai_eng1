from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "My first API is working!"
    })


@app.route("/user", methods=["GET"])
def get_user():
    return jsonify({
        "name": "Samiul",
        "field": "AI Engineering"
    })

#
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.get_json()
#
#     age = data["age"]
#     cholesterol = data["cholesterol"]
#
#     return jsonify({
#         "age": age,
#         "cholesterol": cholesterol,
#         "prediction": "Test prediction"
#     })

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    if "age" not in data:
        return jsonify({
            "error": "Age is required"
        }), 400

    if "cholesterol" not in data:
        return jsonify({
            "error": "Cholesterol is required"
        }), 400

    age = data["age"]
    cholesterol = data["cholesterol"]

    return jsonify({
        "age": age,
        "cholesterol": cholesterol,
        "prediction": "Test prediction"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
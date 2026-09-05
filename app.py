"""
student-ml-api
A minimal Flask inference service used to demonstrate a production-style
MLOps CI/CD workflow (Pull Requests, GitHub Actions, Docker, container
registry publishing).

The "model" here is intentionally trivial (a simple linear function) -
the point of the exercise is the engineering workflow around it, not
the predictive quality of the model itself.
"""

import os

from flask import Flask, jsonify, request

APP_NAME = "student-ml-api"

# Read the application version from the VERSION file so it never has to be
# hard-coded / duplicated in source. Falls back to "0.0.0" if the file is
# missing (e.g. in an unusual runtime context).
_VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")


def _read_version() -> str:
    try:
        with open(_VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "0.0.0"


APP_VERSION = _read_version()

# The model itself has no separate training pipeline in this exercise, so
# its version is tracked as a simple constant here rather than read from a
# file - but it is deliberately independent of APP_VERSION. In a real MLOps
# system the application and the model it serves are versioned and deployed
# on different cadences (e.g. a new model can ship without an app release,
# and vice versa), so the two version numbers must be reported separately.
MODEL_VERSION = "model-1"

app = Flask(__name__)


@app.get("/health")
def health():
    """Liveness / readiness probe."""
    return jsonify(
        {
            "status": "healthy",
            "application": APP_NAME,
            "application_version": APP_VERSION,
            "model_version": MODEL_VERSION,
        }
    ), 200


@app.post("/predict")
def predict():
    """Return a prediction for a numeric input.

    Expected request body: {"value": <number>}
    Expected response:     {"input": <number>, "prediction": <number>}
    """
    payload = request.get_json(silent=True)

    if payload is None or "value" not in payload:
        return jsonify({"error": "Missing required field: 'value'"}), 400

    value = payload["value"]

    # bool is a subclass of int in Python - explicitly reject it so
    # {"value": true} isn't silently treated as a number.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return jsonify({"error": "Field 'value' must be a number"}), 400

    prediction = value * 2

    return jsonify({"input": value, "prediction": prediction}), 200


if __name__ == "__main__":
    # Bind to 0.0.0.0 so the app is reachable from outside a Docker container.
    app.run(host="0.0.0.0", port=5000)

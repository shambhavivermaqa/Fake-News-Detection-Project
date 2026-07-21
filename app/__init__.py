"""Flask application factory for the Fake News Detection web demo."""

import json

from flask import Flask, jsonify, render_template, request, send_from_directory

from src import config
from src.predict import ModelNotTrainedError, predict


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        metrics = None
        if config.METRICS_PATH.exists():
            with open(config.METRICS_PATH) as f:
                metrics = json.load(f)
        return render_template("about.html", metrics=metrics)

    @app.route("/api/predict", methods=["POST"])
    def api_predict():
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        text = (payload.get("text") or "").strip()

        if not title and not text:
            return jsonify({"error": "Please provide a headline or article text."}), 400

        try:
            result = predict(title, text)
        except ModelNotTrainedError as exc:
            return jsonify({"error": str(exc)}), 503
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(result)

    @app.route("/reports/figures/<path:filename>")
    def report_figure(filename):
        return send_from_directory(config.FIGURES_DIR, filename)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    return app

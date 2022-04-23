import os
import random

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}".format(
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from chinese_proverbs.load_data import csv_to_db

csv_to_db()

from chinese_proverbs.models.ProverbsModel import ProverbsModel, db

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        max_count = ProverbsModel.query.count()
        rand_id = random.randint(0, max_count)
        items = ProverbsModel.query.filter(ProverbsModel.p_id == rand_id).first()
        chinese = items.chinese
        pinyin = items.pinyin
        translation = items.p_translation

    return render_template(
        "index.html",
        title="Chinese Proverbs",
        url=os.getenv("URL"),
        chinese=chinese,
        pinyin=pinyin,
        translation=translation
    )


@app.route("/proverbs", methods=["GET"])
def handle_items():
    if request.method == "GET":
        items = ProverbsModel.query.all()
        return jsonify([item.serialize for item in items])
    else:
        return {"message": "failure"}


@app.route("/proverbs/<int:proverb_id>", methods=["GET"])
def handle_item(proverb_id):
    if request.method == "GET":
        items = ProverbsModel.query.filter(ProverbsModel.p_id == proverb_id).first()
        if items:
            items = ProverbsModel.query.filter(ProverbsModel.p_id == proverb_id).all()
            return jsonify([item.serialize for item in items])
        else:
            return jsonify({"error": f"Item {proverb_id} not found"})
    else:
        return {"message": "Request method not implemented"}


@app.route("/proverbs/pinyin/<string:pinyin>", methods=["GET"])
def handle_pinyin(pinyin):
    if request.method == "GET":
        try:
            item = ProverbsModel.query.filter_by(pinyin=pinyin).first_or_404()
            return jsonify(item.serialize)
        except:
            return jsonify({"error": f"Item {pinyin} not found"})
    else:
        return {"message": "Request method not implemented"}


if __name__ == "__main__":
    app.run(debug=True)

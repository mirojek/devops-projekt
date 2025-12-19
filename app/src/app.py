from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

def create_app():
    app = Flask(__name__)

    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "devdb")
    DB_USER = os.getenv("DB_USER", "devuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "devpass")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.User = User

    @app.route("/health", methods=["GET"])
    def health():
        try:
            with app.app_context():
                db.create_all()
            count = db.session.query(User).count()
            return jsonify(status="ok", users_count=count)
        except Exception as e:
            return jsonify(status="error", error=str(e)), 500

    @app.route("/hello", methods=["GET"])
    def hello():
        return jsonify(message="hello devops")

    @app.route("/items", methods=["GET"])
    def items():
        return jsonify(items=[1, 2, 3])

    @app.route("/users", methods=["GET"])
    def list_users():
        users = User.query.all()
        return jsonify(users=[u.to_dict() for u in users])

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
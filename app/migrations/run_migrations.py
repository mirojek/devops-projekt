from app.src import create_app, db
from app.src.app import User

def run():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Migrations: tables created")


if __name__ == "__main__":
    run()
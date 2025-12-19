import os
import csv
from datetime import datetime, timezone
from app.src import create_app, db

app = create_app()
User = app.User

def seed_users():
    users = [
        {"name": "Alicja", "email": "alicja@poczta.com"},
        {"name": "Bartosz", "email": "bartekk@poczta.com"},
        {"name": "Cezary", "email": "czarek@poczta.com"},
        {"name": "Diana", "email": "diana@poczta.com"},
        {"name": "Ewa", "email": "ewa@poczta.com"},
    ]

    with app.app_context():
        db.create_all()
        User.query.delete()
        for u in users:
            user = User(name=u["name"], email=u["email"])
            db.session.add(user)
        db.session.commit()

    return users

def write_files(seed_dir, users):
    os.makedirs(seed_dir, exist_ok=True)

    log_path = os.path.join(seed_dir, "seed.log")
    csv_path = os.path.join(seed_dir, "users.csv")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now(timezone.utc).isoformat()}] "
            f"Seeded {len(users)} users\n"
        )

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email"])
        for u in users:
            writer.writerow([u["name"], u["email"]])

if __name__ == "__main__":
    seed_dir = os.getenv("SEED_OUTPUT_DIR", "/seed_output")
    users = seed_users()
    write_files(seed_dir, users)
    print("Seed completed")

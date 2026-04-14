from database import get_db

db = get_db()
db.execute("DELETE FROM users")
db.commit()

print("All users deleted")
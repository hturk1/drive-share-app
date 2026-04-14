from database import get_db

class AuthService:

    def register(self, email, password, q1, q2, q3):
        db = get_db()
        try:
            db.execute("""
                INSERT INTO users(email, password, q1, q2, q3)
                VALUES (?, ?, ?, ?, ?)
            """, (email, password, q1, q2, q3))
            db.commit()
            return True, "Registered successfully"
        except:
            return False, "User already exists"

    def login(self, email, password):
        db = get_db()
        user = db.execute("""
            SELECT * FROM users WHERE email=? AND password=?
        """, (email, password)).fetchone()

        if user:
            return True, user
        return False, None

    def recover_check(self, email, answers):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if not user:
            return False

        return (user["q1"] == answers[0] and
                user["q2"] == answers[1] and
                user["q3"] == answers[2])
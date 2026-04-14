from database import get_db

class NotificationService:

    def send(self, user_id, message):
        db = get_db()

        db.execute("""
            INSERT INTO notifications (user_id, message)
            VALUES (?, ?)
        """, (user_id, message))

        db.commit()

    def get(self, user_id):
        db = get_db()

        return db.execute("""
            SELECT * FROM notifications
            WHERE user_id=?
            ORDER BY id DESC
        """, (user_id,)).fetchall()
messages = []

from database import get_db

class MessageService:

    def send(self, from_id, to_user_id, text):
        db = get_db()

        db.execute("""
            INSERT INTO notifications (user_id, message)
            VALUES (?, ?)
        """, (
            to_user_id,
            f"FROM:{from_id}|{text}"
        ))

        db.commit()
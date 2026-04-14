from database import get_db
from patterns.observer import WatchSubject, WatchObserver
from notification_service import NotificationService

class WatchService:

    def notify_watchers(self, car):

        db = get_db()

        watches = db.execute("""
            SELECT * FROM watches WHERE car_id=?
        """, (car["id"],)).fetchall()

        subject = WatchSubject()

        for w in watches:
            observer = WatchObserver(
                w["user_id"],
                w["max_price"],
                NotificationService()
            )
            subject.attach(observer)

        subject.notify(car)
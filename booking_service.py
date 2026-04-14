from database import get_db
from notification_service import NotificationService
from patterns.observer import WatchSubject, WatchObserver
from watch_service import WatchService

watch_service = WatchService()

notifications = NotificationService()

class BookingService:

    def book_car(self, car_id, user_id, start_date, end_date):
        db = get_db()

        # CHECK FOR OVERLAPPING BOOKINGS
        conflict = db.execute("""
            SELECT * FROM bookings
            WHERE car_id = ?
            AND (
                start_date <= ? AND end_date >= ?
            )
        """, (car_id, end_date, start_date)).fetchone()

        if conflict:
            return False, "Car already booked for those dates"

        # get car price (dynamic)
        car = db.execute(
            "SELECT * FROM cars WHERE id=?",
            (car_id,)
        ).fetchone()

        # save booking
        db.execute("""
            INSERT INTO bookings (car_id, user_id, start_date, end_date, price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            car_id,
            user_id,
            start_date,
            end_date,
            car["price"]
        ))

        db.commit()
        
        notifications.send(
            car["owner_id"],
            f"Booking request for {car['model']} from user {user_id}"
        )

        notifications.send(
            user_id,
            f"You requested booking for {car['model']}"
        )

        return True, f"Booking requested successfully for ${car['price']}"
from database import get_db
from patterns.observer import WatchSubject, WatchObserver
from notification_service import NotificationService
from patterns.builder import CarBuilder


subject = WatchSubject()
notifications = NotificationService()

class CarService:

    def add_car(self, owner_id, model, year, mileage, location, price, available):

        car = (CarBuilder()
            .set_owner(owner_id)
            .set_model(model)
            .set_year(year)
            .set_mileage(mileage)
            .set_location(location)
            .set_price(price)
            .set_available(available)
            .build())

        db = get_db()
        db.execute("""
            INSERT INTO cars(owner_id, model, year, mileage, location, price, available)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            car.owner_id,
            car.model,
            car.year,
            car.mileage,
            car.location,
            car.price,
            car.available
        ))
        db.commit()

    def get_all_cars(self):
        db = get_db()
        return db.execute("SELECT * FROM cars").fetchall()

    def get_my_cars(self, owner_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM cars WHERE owner_id=?",
            (owner_id,)
        ).fetchall()

    def update_car(self, car_id, price, available):
        db = get_db()
        db.execute("""
            UPDATE cars
            SET price=?, available=?
            WHERE id=?
        """, (price, available, car_id))
        db.commit()

    def get_car_by_id(self, car_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM cars WHERE id=?",
            (car_id,)
        ).fetchone()
    
    def search_by_location(self, location):
        db = get_db()

        return db.execute("""
            SELECT * FROM cars
            WHERE location LIKE ?
        """, ('%' + location + '%',)).fetchall()
    
    def update_price(self, car_id, new_price):
        db = get_db()

        db.execute("""
            UPDATE cars SET price=? WHERE id=?
        """, (new_price, car_id))

        db.commit()

        car = db.execute("""
            SELECT * FROM cars WHERE id=?
        """, (car_id,)).fetchone()
        
        from watch_service import WatchService
        watch_service = WatchService()

        watch_service.notify_watchers(car) #once price is change user get notified 
    
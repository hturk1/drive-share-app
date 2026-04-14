class Car:
    def __init__(self):
        self.owner_id = None
        self.model = None
        self.year = None
        self.mileage = None
        self.location = None
        self.price = None
        self.available = None


class CarBuilder:
    def __init__(self):
        self.car = Car()

    def set_owner(self, owner_id):
        self.car.owner_id = owner_id
        return self

    def set_model(self, model):
        self.car.model = model
        return self

    def set_year(self, year):
        self.car.year = year
        return self

    def set_mileage(self, mileage):
        self.car.mileage = mileage
        return self

    def set_location(self, location):
        self.car.location = location
        return self

    def set_price(self, price):
        self.car.price = price
        return self

    def set_available(self, available):
        self.car.available = available
        return self

    def build(self):
        return self.car
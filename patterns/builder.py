class Car:
    def __init__(self):
        self.model = None
        self.price = None
        self.owner_id = None


class CarBuilder:
    def __init__(self):
        self.car = Car()

    def set_model(self, model):
        self.car.model = model
        return self

    def set_price(self, price):
        self.car.price = price
        return self

    def set_owner(self, owner_id):
        self.car.owner_id = owner_id
        return self

    def build(self):
        return self.car
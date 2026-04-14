class WatchSubject:

    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, car):
        for obs in self.observers:
            obs.update(car)


class WatchObserver:

    def __init__(self, user_id, max_price, notification_service):
        self.user_id = user_id
        self.max_price = float(max_price)
        self.notifications = notification_service


    def update(self, car):

        price = float(car["price"])
        available = int(car["available"])

        # Price condition
        if price <= self.max_price:
            self.notifications.send(
                self.user_id,
                f"{car['model']} dropped to ${price}"
            )

        # Availability condition
        if available == 1:
            self.notifications.send(
                self.user_id,
                f"{car['model']} is now available!"
            )
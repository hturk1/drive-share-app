from patterns.proxy import PaymentProxy

class PaymentService:
    def __init__(self):
        self.proxy = PaymentProxy()

    def pay(self, amount):
        return self.proxy.process(amount)
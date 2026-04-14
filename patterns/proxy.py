class RealPayment:

    def process(self, amount):
        # simulate real payment processing
        return f"Payment of ${amount} completed"


class PaymentProxy:

    def __init__(self):
        self.real = RealPayment()

    def process(self, amount):
        # Proxy adds control/security layer
        if amount <= 0:
            return "Invalid payment amount"

        print("Proxy: validating payment...")

        return self.real.process(amount)
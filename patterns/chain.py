class Handler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, data):
        if self.next:
            return self.next.handle(data)


class Q1Handler(Handler):
    def handle(self, data):
        if data["input_q1"].strip().lower() == data["db_q1"].strip().lower():
            return super().handle(data)
        return False


class Q2Handler(Handler):
    def handle(self, data):
        if data["input_q2"].strip().lower() == data["db_q2"].strip().lower():
            return super().handle(data)
        return False


class Q3Handler(Handler):
    def handle(self, data):
        if data["input_q3"].strip().lower() == data["db_q3"].strip().lower():
            return True
        return False
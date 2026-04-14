class Mediator:
    def notify(self, sender, event):
        print(f"[MEDIATOR] {sender} -> {event}")
class Mediator:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def notify(self, sender, event, user_id=None):
        message = f"[{sender}] {event}"

        if user_id:
            self.notification_service.send(user_id, message)
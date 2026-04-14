class Mediator:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def notify(self, sender, event, user_id=None):
        message = f"[{sender}] {event}"

        if user_id:
            self.notification_service.send(user_id, message)

    # centralized messaging
    def send_message(self, from_id, to_id, text):
        msg = f"FROM:{from_id}|{text}"
        self.notification_service.send(to_id, msg)

    # system events (watch + booking + updates)
    def system_event(self, event, user_ids):
        for uid in user_ids:
            self.notification_service.send(uid, f"[SYSTEM] {event}")
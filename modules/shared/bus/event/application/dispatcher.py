from .registry import CLASS_SUBSCRIBERS

class Dispatcher:

    @staticmethod
    def dispatch(event: dict):
        print(CLASS_SUBSCRIBERS)
        event_name = event.get("event_name")
        handlers = CLASS_SUBSCRIBERS.get(event_name)

        if handlers:
            for handler in handlers:
                handler = handler()
                handler.handle(event)

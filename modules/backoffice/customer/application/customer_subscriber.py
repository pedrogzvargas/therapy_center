from modules.shared.bus.event.application import subscriber


@subscriber("backoffice.customer.created")
class CustomerSubscriber:

    def handle(self, event):
        print("CustomerSubscriber", event)

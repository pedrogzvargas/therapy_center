import importlib

SUBSCRIBERS_MODULES = [
    "modules.backoffice.customer.application.customer_subscriber",
]

def load_subscribers():
    for module in SUBSCRIBERS_MODULES:
        importlib.import_module(module)

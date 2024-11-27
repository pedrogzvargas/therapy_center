from modules.passenger.infraestructure import PassengerCreatedSubscriber
from modules.passenger.infraestructure import PassengerPatchedSubscriber


message_handler = {
    "reservation_app.passenger_created": PassengerCreatedSubscriber,
    "reservation_app.passenger_patched": PassengerPatchedSubscriber,
}

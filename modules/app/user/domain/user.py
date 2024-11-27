from modules.shared.aggregate_root.domain import AggregateRoot


class User(AggregateRoot):
    """
    User entity
    """

    def __init__(self, id, name, last_name, username, password, is_active, second_last_name=None):
        self._id = id
        self._name = name
        self._last_name = last_name
        self._second_last_name = second_last_name
        self._username = username
        self._password = password
        self._is_active = is_active

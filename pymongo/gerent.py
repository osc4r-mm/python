from user import User

class Gerent(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, rol="gerent")
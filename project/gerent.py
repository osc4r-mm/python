from user import User
from db import get_db

class Gerent(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, rol="gerent")
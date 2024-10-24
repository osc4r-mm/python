from user import User

class Administrative(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, rol="administratiu")

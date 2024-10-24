from user import User
from routine import Routine
import tools

class Trainer(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, rol="entrenador")

    def create_routine(self):
        # CONST
        WEEK_MENU = {
        "1": "dilluns",
        "2": "dimarts",
        "3": "dimecres",
        "4": "dijous",
        "5": "divendres",
        "6": "dissabte",
        "7": "diumenge"
        }

        ROOM_MENU = {
        "1": "activitats dirigides",
        "2": "musculacio"
        }

        name = tools.get_valid_input("Introdueix el nom (1-55 caràcters): ", lambda user_input: tools.input_string(user_input, 1, 55))
        description = tools.get_valid_input("Introdueix una descripcio (0-255 caràcters): ", lambda user_input: tools.input_string(user_input, 0, 255))
        trainer = {"nom": self.name,
                   "email": self.email}
        
        room = tools.get_valid_menu(ROOM_MENU)
        day = tools.get_valid_menu(WEEK_MENU)
        hour = ""
        durada = ""
        horari = {room, day, hour, }
        
        durada = ""
        Routine.add_routine(name, description, trainer, horari, durada)
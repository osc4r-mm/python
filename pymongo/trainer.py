from user import User
from routine import Routine
import tools

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

class Trainer(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, rol="entrenador")

    def create_routine(self):
        name = tools.get_valid_input("Introdueix el nom (1-55 caràcters): ", lambda user_input: tools.input_string(user_input, 1, 55))
        description = tools.get_valid_input("Introdueix una descripcio (0-255 caràcters): ", lambda user_input: tools.input_string(user_input, 0, 255))
        trainer = {"nom": self.name,
                   "email": self.email}
        
        recommendations = tools.get_valid_input("Introdueix recomanacions (0-255 caràcters): ", lambda user_input: tools.input_string(user_input, 0, 255))

        room = tools.get_valid_menu(ROOM_MENU)
        day = tools.get_valid_menu(WEEK_MENU)
        hour = tools.get_valid_input("Introdueix el nom (1-55 caràcters): ", lambda user_input: tools.input_string(user_input, 0, 23))
        durada = 60
        horari = {
            "habitacio": room, 
            "dia": day, 
            "hora": hour, 
            "durada": durada,
            "recomendacions": recommendations
            }
        
        durada = 60
        routine = Routine(name, description, trainer, horari, durada)
        routine.add_routine()
        print(f"Rutina '{name}' creada correctament.")

    def manage_attendance(self, routine_name):
        """ Consultar y gestionar asistencia """
        MANAGE_USER_MENU = {
        "1": "afegir",
        "2": "eliminar",
        "3": "exit"
        }
        
        room = tools.get_valid_menu(ROOM_MENU)
        day = tools.get_valid_menu(WEEK_MENU)
        hour = tools.get_valid_input("Introdueix una hora (de 0 a 23): ", lambda user_input: tools.input_int(user_input, 0, 23))
        horari = {
            "habitacio": room,
            "dia": day,
            "hora": hour
        }
        
        routine = Routine(routine_name, "", "", horari)
        print("Usuaris inscrits actualment:", routine.get_routine_list())
        
        option = tools.show_menu(MANAGE_USER_MENU)

        # Obtenim l'id de l'usuari a traves del seu email
        user_email = tools.get_valid_input("Introdueix el email de l'usuari: ", tools.input_email)
        user_id = self.db_users.find_one({"email": user_email}, {"_id": 1})["_id"]

        if option == "add":
            routine.add_user_to_routine(user_id)
        elif option == "remove":
            routine.remove_user_from_routine(user_id)
            
import tools
from db import get_db


# Classe Usuari Bàsic
class User:
    def __init__(self, name, email, passwd, rol="usuari"):
        self.name = name
        self.email = email
        self.passwd = tools.encrypt_passwd(passwd) # Encriptada
        self.rol = rol
        self.db_users = get_db("users")

    def show_menu_user(self):
        """
            Mostra el menú basat en el rol de l'usuari.

            Args:
                role (str): Rol de l'usuari (p.ex., 'usuari', 'entrenador').

            Returns:
                str: La opció escollida per l'usuari.
        """
        USER_MENU = {
            "usuari": {
            "1": "inscriure rutina",
            "2": "sortir"
            },
            "entrenador": {
            "1": "crear rutina",
            "2": "assigna horari",
            "3": "gestio assistencia",
            "5": "sortir"
            },

            "administratiu": {
            "1": "sortir"
            },
            "gerent": {
            "1": "sortir"
            }
        }

        option = tools.get_valid_menu(USER_MENU[self.rol])
        return option


    def register_user(self):
        """
        Assegura que l'usuari no existeix i si es aixi el registra a la base de dades
        """

        if self.db_users.find_one({"email": self.email}):
            raise Exception("Error: L'usuari ja existeix.")
    
        new_user = {
            "name": self.name,
            "email": self.email,
            "passwd": self.passwd,
            "rol": self.rol
        }
        
        self.db_users.insert_one(new_user)
        
    @staticmethod
    def login(email, passwd):
        """
        Inicia sessió de l'usuari comprovant el correu i la contrasenya
        """
        from trainer import Trainer
        from administrative import Administrative
        from gerent import Gerent
        db = get_db()
        users_collection = db['users']
        user = users_collection.find_one({"email": email})
        
        if user and tools.check_passwd_hash(passwd, user['passwd']):
            name = user['name']
            role = user['rol']
            
            if role == "usuari":
                return User(name, email, passwd)
            elif role == "entrenador":
                return Trainer(name, email, passwd)
            elif role == "administratiu":
                return Administrative(name, email, passwd)
            elif role == "gerent":
                return Gerent(name, email, passwd)
        else:
            return None


    @staticmethod
    def logout():
        """
        Tanca la sessió de l'usuari
        """
        print("Sessió tancada correctament.")
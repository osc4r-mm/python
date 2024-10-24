import tools
from db import get_db


# Classe Usuari Bàsic
class User:
    def __init__(self, name, email, passwd, rol="usuari"):
        self.name = name
        self.email = email
        self.passwd = tools.encrypt_passwd(passwd) # Encriptada
        self.rol = rol
        self.db = get_db()

    def register_user(self):
        """
        Assegura que l'usuari no existeix i si es aixi el registra a la base de dades
        """
        users_collection = self.db['users']

        if users_collection.find_one({"email": self.email}):
            raise Exception("Error: L'usuari ja existeix.")
    
        new_user = {
            "name": self.name,
            "email": self.email,
            "passwd": self.passwd,
            "rol": self.rol
        }
        
        users_collection.insert_one(new_user)
        
    @staticmethod
    def login(email, passwd):
        """
        Inicia sessió de l'usuari comprovant el correu i la contrasenya
        """
        db = get_db()
        users_collection = db['users']
        user = users_collection.find_one({"email": email})
        
        if user and tools.check_passwd_hash(passwd, user['passwd']):
            return user
        else:
            return None

    @staticmethod
    def logout():
        """
        Tanca la sessió de l'usuari
        """
        print("Sessió tancada correctament.")
import tools
from db import get_db

class Routine():
    def __init__(self, name, description, trainer, horari, recommendations, durada=60):
        self.name = name
        self.description = description
        self.trainer = trainer
        self.horari = horari
        self.recommendations = recommendations
        self.durada = durada
        self.db_routines = get_db("routines")

    def add_routine(self):
        """
        Mete la rutina en mongodb
        """
        new_routine = {
            "nom": self.name,
            "descripcio": self.description,
            "entrenador": self.trainer,
            "horari": self.horari,
            "recomendacions": self.recommendations,
            "durada": self.durada
        }

        self.db_routines.insert_one(new_routine)
    
    def list_routines(self):
        """Obtener i mostrar tots els identificadors de les rutines."""
        routines = self.db_routines.find({}, {"_id": 1, "nom": 1, "horari": 1})
        print("Llista de rutines:")
        for routine in routines:
            print(f"ID: {routine['_id']} - Nom: {routine['nom']}")

    def add_user_to_routine(self, user_id):
        """ Afegir un usuari a la llista d'asistencia """
        self.db_routines.update_one(
            {"name": self.name, "horari": self.horari},
            {"$addToSet": {"attendance": user_id}}
        )

    def remove_user_from_routine(self, user_id):
        """ Eliminar un usuari de la llista d'asistencia """
        self.db_routines.update_one(
            {"name": self.name, "horari": self.horari},
            {"$pull": {"attendance": user_id}}
        )

    def get_routine_list(self):
        """ Obtenir la llista d'usuaris inscrits en aquesta rutina """
        routine = self.db_routines.find_one({"name": self.name, "horari": self.horari})
        return routine.get("attendance", [])

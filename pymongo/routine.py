import tools
from db import get_db

class Routine():
    def __init__(self, name, description, trainer, horari, durada=60):
        self.name = name
        self.description = description
        self.trainer = trainer
        self.horari = horari
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
            "durada": self.durada
        }

        # Informacio de l'horari
        habitacio = self.horari["habitacio"]
        dia = self.horari["dia"]
        hora = self.horari["hora"]
        
        # Rang de temps a comprovar
        start_time = hora - 1
        end_time = start_time + 1

        # Comprova si hi ha alguna rutina en el rang de temps especificat
        conflict = self.db_routines.find_one({
            "horari.habitacio": habitacio,
            "horari.dia": dia,
            "horari.hora": {"$gte": start_time // 60, "$lt": end_time // 60}}
        )

        if conflict is None:
            self.db_routines.insert_one(new_routine)
        else:
            print("Error:")

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

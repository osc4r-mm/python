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
        lo mete en mongodb
        """
        new_routine = {
            "name": self.name,
            "description": self.description,
            "trainer": self.trainer,
            "horari": self.horari
        }

        self.db_routines.insert_one(new_routine)
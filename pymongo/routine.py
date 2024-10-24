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

    def add_routine(self, name, description, trainer, horari):
        """
        lo mete en mongodb
        """
        return Routine(name, description, trainer, horari)
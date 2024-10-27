from user import User
from trainer import Trainer
from administrative import Administrative
from gerent import Gerent
import tools

def register():
    """
    Registra un usuari a una base de dades de mongodb sol·licitant a l'usuari 
    que introdueixi el seu nom, correu electrònic, contrasenya i rol, i després 
    crea un nou usuari a la base de dades si les dades són vàlides.
    """
    # CONST
    ROL_MENU = {
        "1": "usuari",
        "2": "entrenador",
        "3": "administratiu",
        "4": "gerent"
    }

    # Inputs
    print("\n--- Registre d'Usuari ---")
    name = tools.get_valid_input("Introdueix el teu nom (3-20 caràcters): ", lambda user_input: tools.input_string(user_input, 3, 20))
    email = tools.get_valid_input("Introdueix el teu correu electrònic: ", tools.input_email)
    passwd = tools.get_valid_input("Introdueix la teva contrasenya (mínim 8 caràcters, 1 minúscula, 1 majúscula, 1 especial): ", tools.input_passwd)

    print("Selecciona el rol:")
    rol_option = tools.show_menu(ROL_MENU)
    rol = ROL_MENU.get(rol_option)

    if rol == "usuari":
        user = User(name, email, passwd)
    elif rol == "entrenador":
        user = Trainer(name, email, passwd)
    elif rol == "administratiu":
        user = Administrative(name, email, passwd)
    elif rol == "gerent":
        user = Gerent(name, email, passwd)
    else:
        print("Rol invàlid. Assignant rol per defecte: Usuari Gimnàs.")
        user = User(name, email, passwd)
    
    try:
        user.register_user()
        print(f"Usuari {user.name} registrat correctament com a {user.rol}.")
    except Exception as e:
        print(e)

def login():
    """
    Inicia sessió d'un usuari al sistema sol·licitant a l'usuari el seu correu 
    electrònic i contrasenya, i comprova les credencials amb la base de dades. 
    Si les credencials són vàlides, s'inicia la sessió i s'emmagatzema la 
    informació de l'usuari actual
    """
    global current_user

    print("\n--- Iniciar Sessió ---")
    email = input("Correu electrònic: ")
    passwd = input("Contrasenya: ")
    
    user = User.login(email, passwd)
    if user:
        current_user = user
        print(f"Inici de sessió correcte. Benvingut/da {user.name} ({user.rol}).")
    else:
        print("Credencials incorrectes.")

def main():
    # CONST
    START_MENU = {
        "1": "registrar-se",
        "2": "iniciar sessió",
        "3": "sortir"
    }

    # Variables globals
    global current_user
    current_user = None

    # variables
    menu = True

    # Menu d'inici
    while menu:
        if current_user == None:
            option = tools.show_menu(START_MENU)
            if option == "1":
                register()
            elif option == "2":
                login()
            elif option == "3":
                print("Sortint.")
                menu = False
            else:
                print("Opció invàlida. Intenta-ho de nou.")
        else:
            option = current_user.show_menu_user()
            if current_user.rol == "usuari":
                if option == "1":
                    pass
                elif option == "2":
                    current_user.logout()
                    current_user = None

            elif current_user.rol == "entrenador":
                if option == "1":
                    current_user.create_routine()
                elif option == "2":
                    current_user.assign_horari()
                elif option == "3":
                    current_user.manage_attendance()
                elif option == "4":
                    current_user.logout()
                    current_user = None


            elif current_user["rol"] == "administratiu":
                print("hola")
            elif current_user["rol"] == "gerent":
                print("hola")

if __name__ == "__main__":
    main()
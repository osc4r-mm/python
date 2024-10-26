import hashlib

def get_valid_input(prompt, validation_func, check=True):
    """
    Funció genèrica per obtenir una entrada vàlida de l'usuari amb una funcio de validacio

    Args:
        prompt (str): El missatge que es mostra a l'usuari per demanar l'entrada
        validation_func (callable): Funció que valida l'entrada de l'usuari

    Returns:
        str: L'entrada vàlidada de l'usuari.
    """
    while check:
        try:
            user_input = input(prompt)
            return validation_func(user_input)
        except Exception as e:
            print(e)

def input_string(name, min, max):
    """
    Funcio que demana un nom a l'usuari, l'accepta si compleix el següent: 
    - Entre 3 i 20 caracters
    
    Args:
        name (str): nom introduit de l'usuari

    Returns:
        str: El nom validat per l'usuari
    """
    if min <= len(name) <= max:
        return name
    else:
        raise Exception(f"Error: El nom ha de tenir entre {min} i {max} caràcters.")

def input_int(num, min, max):
    if min <= num <= max:
        return num
    else:
        raise Exception(f"Error: El numero ha de ser entre {min} i {max}.")
    
def input_email(email):
    """
    Funcio que demana un correu electronic a l'usuari i el valida si:
    · Email 
        - Conte una @

    · L'usuari (pre domini) 
        - Entre 4 i 20 caràcters 
        - Només pot contenir lletres, números, punts i guions baixos
    
    · El domini
        - Ha de ser un domini vàlid (gmail, hotmail, outlook, lacetania, prova) 
        - Seguit d'un sufix vàlid (com, net, cat)

    Args:
        email (str): Email introduit de l'usuari

    Returns:
        str: El correu electrònic validat
    """
    valid_domain = {
        "gmail": ["com"],
        "hotmail": ["com"],
        "outlook": ["com"],
        "lacetania": ["com", "cat"],
        "prova": ["cat", "net"]
    }

    # El email conte un @
    if email.count('@') != 1:
        raise Exception("Error: El correu ha de contenir exactament un '@'.")
    
    pre_domain, domain = email.split('@')

    """ Pre domini """
    # Te entre 3 y 20 caracters
    if len(pre_domain) < 3 or len(pre_domain) > 20:
        raise Exception("Error: La part abans de l'@ ha de tenir entre 3 i 20 caracters.")
    
    # Es un caracter alfanumeric o un "." o un "_"
    if not all(c.isalnum() or c in '._' for c in pre_domain):
        raise Exception("Error: La part abans de l'@ nomes pot contenir lletres, numeros, punts (.) o guions baixos (_).")
    
    try:
        domain_name, sufix = domain.split('.')
    except:
        raise Exception("Error: El domini ha de tenir un .")

    """ Domini """
    # El domini esta al diccionari de dominis valids
    if domain_name not in valid_domain:
        raise Exception(f"Error: El domini '{domain_name}' no es valid. Ha de ser un dels següents: gmail, hotmail, outlook, lacetania, prova.")

    # El sufix equival al domini correcte
    if sufix not in valid_domain[domain_name]:
        raise Exception(f"Error: El sufix '{sufix}' no es valid per al domini '{domain_name}'. Ha de ser un dels següents: {', '.join(valid_domain[domain_name])}.")
    
    return email


def input_passwd(passwd):
    """
    Funció que demana una contrasenya a l'usuari i la valida segons els criteris indicats:
    - Mínim 8 caràcters
    - Almenys 1 minúscula
    - Almenys 1 majúscula
    - Almenys 1 numero
    - Almenys 1 caràcter especial

    Args:
        passwd (str): Contrasenya introduida de l'usuari

    Returns:
        str: La contrasenya validada
    """
    # CONST
    SPECIAL_CHARS = "!@#$%^&*(),.?\":{}|<>"

    if len(passwd) < 8:
        raise Exception("Error: La contrasenya ha de tenir almenys 8 caràcters.")
    
    if not any(c.islower() for c in passwd):
        raise Exception("Error: La contrasenya ha de contenir almenys una lletra minúscula.")
    
    if not any(c.isupper() for c in passwd):
        raise Exception("Error: La contrasenya ha de contenir almenys una lletra majúscula.")
    
    if not any(c.isdigit() for c in passwd):
        raise Exception("Error: La contrasenya ha de contenir almenys un número.")

    if not any(c in SPECIAL_CHARS for c in passwd):
        raise Exception("Error: La contrasenya ha de contenir almenys un caràcter especial (p.ex. !@#$%^&*).")

    return passwd
    
def encrypt_passwd(passwd):
    """
    Funció que encripta una contrasenya utilitzant SHA-256
    
    Args:
        passwd (str): La contrasenya de l'usuari
    
    Returns:
        str: El hash de la contrasenya
    """
    return hashlib.sha256(passwd.encode()).hexdigest()


def check_passwd_hash(passwd_user, hash_save):
    """
    Funció que valida una contrasenya comparant el seu hash amb el que està desat
    
    Args:
        passwd_user (str): La contrasenya que l'usuari introdueix
        hash_save (str): El hash de la contrasenya desada anteriorment
    
    Returns:
        bool: Retorna True si la contrasenya és vàlida o False si no
    """
    # Encriptem la contrasenya introduïda per l'usuari i la comparem amb l'hash desat.
    hash_user = hashlib.sha256(passwd_user.encode()).hexdigest()
    return hash_user == hash_save

def get_valid_menu(MENU, check=True):
    """
    Funció genèrica per obtenir una entrada vàlida de l'usuari amb una funcio de validacio

    Args:
        prompt (str): El missatge que es mostra a l'usuari per demanar l'entrada
        validation_func (callable): Funció que valida l'entrada de l'usuari

    Returns:
        str: L'entrada vàlidada de l'usuari.
    """
    while check:
        option = show_menu(MENU)
        if option in MENU.keys():
            return option
        raise Exception(f"Error: '{option}' no esta dintre de les opcions")

def show_menu(options):
    """
    Mostra un menú a partir d'un diccionari

    Args:
        opcions (dict): Diccionari amb les opcions del menú.
                        Les claus són les opcions a mostrar i els valors són
                        les descripcions d'aquestes opcions
    """
    print("\n=== Menú ===")
    for option, description in options.items():
        print(f"{option}. {description.capitalize()}")
    eleccio = input("Selecciona una opció: ")
    return eleccio
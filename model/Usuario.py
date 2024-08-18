class Usuario:
    # Constructor.
    def __init__(self, id:int, nombre1:str, usuario:str, contrasena:str, correo:str, cc:int, rol_id:int, nombre2:str="", apellido1:str="", apellido2:str=""):
        self.id = id
        self.nombre1 = nombre1
        self.nombre2 = nombre2
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.usuario = usuario
        self.contrasena = contrasena
        self.correo = correo
        self.cc = cc
        self.rol_id = rol_id
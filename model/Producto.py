class Producto:
    def __init__(self, id:int, nombre:str, precio:float, cantidad:int, descripcion:str=""):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descripcion = descripcion
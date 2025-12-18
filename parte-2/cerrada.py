# Esta estructura guarda los nodos que ya hemos visitado completamente
# (es decir, ya hemos mirado todos sus vecinos).
#
# La usamos para no volver a explorar un nodo que ya exploramos antes,
# lo cual seria perder el tiempo.
#
# Es muy sencilla: solo un diccionario donde la clave es el nodo
# y el valor es el coste con el que lo cerramos.

class Cerrada:
    """
    Lista cerrada para registrar los nodos que ya hemos explorado.
    
    Cuando "cerramos" un nodo, significa que ya lo hemos sacado de la
    lista abierta y hemos mirado todos sus vecinos.
    
    Guardamos tambien el coste g con el que lo cerramos, por si acaso
    encontramos un camino mejor despues (aunque con A* bien implementado
    esto no deberia pasar si la heuristica es consistente).
    """
    
    def __init__(self):
        """
        Inicializa la lista cerrada vacia.
        """
        # Diccionario: nodo -> coste con el que lo cerramos
        self.cerrados = {}
    
    
    def anadir(self, nodo, coste_acumulado):
        """
        Anade un nodo a la lista cerrada.
        
        Parametros:
            nodo: el identificador del nodo
            coste_acumulado: el coste g con el que llegamos a este nodo
        """
        self.cerrados[nodo] = coste_acumulado
    
    
    def contiene(self, nodo):
        """
        Comprueba si un nodo ya esta en la lista cerrada.
        
        Devuelve:
            True si el nodo ya fue cerrado, False si no
        """
        esta_dentro = nodo in self.cerrados
        return esta_dentro
    
    
    def coste(self, nodo):
        """
        Devuelve el coste con el que cerramos un nodo.
        
        Devuelve:
            El coste g, o None si el nodo no esta cerrado
        """
        return self.cerrados.get(nodo)
    
    
    def vacia(self):
        """
        Comprueba si la lista cerrada esta vacia.
        """
        cantidad = len(self.cerrados)
        return cantidad == 0

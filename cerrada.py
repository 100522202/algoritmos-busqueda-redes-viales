# Lista cerrada sencilla para registrar los nodos que ya se han expandido
class Cerrada:
    def __init__(self):
        """
        Inicializa la estructura 'Cerrada'
        """
        self.cerrados = {}  # Diccionario que almacena los nodos ya visitados o cerrados.

    def anadir(self, nodo, coste_acumulado):
        """
        Añade un nodo a la lista cerrada.
        """
        self.cerrados[nodo] = coste_acumulado  # Registramos el nodo como cerrado.

    def contiene(self, nodo):
        """
        Devuelve True si el nodo ya está en la lista cerrada.
        """
        return nodo in self.cerrados  # Comprobamos si el nodo está en 'cerrados'.

    def coste(self, nodo):
        """
        Devuelve el coste acumulado almacenado para un nodo cerrado.
        """
        return self.cerrados.get(nodo)  # Recuperamos el coste guardado para ese nodo.

    def vacio(self):
        """
        Indica si la lista cerrada está vacía.
        """
        return len(self.cerrados) == 0  # True si no hay ningún nodo.

import time
from abierta import Abierta
from cerrada import Cerrada


class Algoritmo:
    def __init__(self, grafo, inicio, fin):
        """
        Inicializa el algoritmo con:
        - grafo: estructura que contiene nodos, arcos y coordenadas.
        - inicio: nodo desde donde parte la búsqueda.
        - fin: nodo objetivo al que queremos llegar.
        """
        self.grafo = grafo
        self.inicio = inicio
        self.fin = fin  #

    def reconstruir_camino(self, padres, nodo_final):
        """
        Reconstruye el camino final desde el nodo inicial hasta el nodo_final.
        """
        #Lista donde guardaremos el camino.
        camino = []
        #Empezamos desde el final
        actual = nodo_final

        # Retrocedemos mientras exista un nodo padre.
        while actual is not None:
            camino.append(actual)  # Añadimos el nodo al camino.
            actual = padres.get(actual)  # Saltamos al padre del nodo actual.

        camino.reverse()  # El camino está al revés, así que lo invertimos.
        return camino

    def dijkstra(self):
        """
        Implementará el algoritmo de Dijkstra.
        """
        inicio_t = time.time()  # Guardamos el tiempo de inicio.

        # Aquí irá la implementación completa de Dijkstra.
        # Por ahora, está vacío.
        # TODO: implementar Dijkstra aquí.

        tiempo_total = time.time() - inicio_t  # Calculamos tiempo transcurrido.
        return None, None, 0, tiempo_total  # Devolvemos valores vacíos.

    def fuerza_bruta(self):
        """
        Implementará un sistema de búsqueda por fuerza bruta.
        """
        inicio_t = time.time()  # Guardamos hora de inicio.

        # Aquí irá la implementación de fuerza bruta.
        # TODO: implementar fuerza bruta aquí.

        tiempo_total = time.time() - inicio_t
        return None, None, 0, tiempo_total

    def heuristica(self, nodo):
        """
        Calcula la heurística para un nodo
        """
        return self.grafo.distancia(nodo,
                                    self.fin)  # Llamada directa al grafo.

    def a_estrella(self):
        """
        Ejecuta el algoritmo A*
        """
        inicio_t = time.time()  # Inicio de medición del tiempo.

        abierta = Abierta()  # Lista abierta (nodos por explorar).
        cerrada = Cerrada()  # Lista cerrada (nodos ya explorados).
        padres = {}  # Diccionario nodo -> padre para reconstruir camino.
        expansiones = 0  # Contador de expansiones de nodos.

        # TODO: implementar aquí la lógica de A*.

        tiempo_total = time.time() - inicio_t
        return None, None, expansiones, tiempo_total

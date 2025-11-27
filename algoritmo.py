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
        Ejecuta el algoritmo A* y devuelve:
        - camino óptimo
        - coste total
        - número de expansiones
        - tiempo de ejecución
        """
        inicio_t = time.time()

        abierta = Abierta()  # Lista de nodos pendientes
        cerrada = Cerrada()  # Nodos ya explorados
        padres = {}  # Para reconstruir el camino
        g_cost = {}  # Coste real g(n)
        expansiones = 0

        # Coste inicial
        g_cost[self.inicio] = 0
        f_inicial = g_cost[self.inicio] + self.heuristica(self.inicio)

        # Insertamos el nodo inicial en OPEN
        abierta.push(self.inicio, f_inicial, g_cost[self.inicio])
        padres[self.inicio] = None

        # Bucle principal
        while True:
            extraido = abierta.pop()
            if extraido is None:
                break

            nodo, f_actual, g_actual = extraido

            # Si ya está en cerrada con igual o mejor g, ignoramos la entrada obsoleta
            if cerrada.contiene(nodo):
                g_cerrado = cerrada.coste(nodo)
                if g_cerrado is not None and g_actual >= g_cerrado:
                    continue
                # Reabrimos el nodo si encontramos un camino mejor
                cerrada.cerrados.pop(nodo, None)

            expansiones += 1

            if nodo == self.fin:
                camino = self.reconstruir_camino(padres, nodo)
                tiempo_total = time.time() - inicio_t
                return camino, g_actual, expansiones, tiempo_total

            cerrada.anadir(nodo, g_actual)

            for vecino, coste_arco in self.grafo.vecinos(nodo):
                g_nuevo = g_actual + coste_arco

                if cerrada.contiene(vecino):
                    if g_nuevo < cerrada.coste(vecino):
                        cerrada.cerrados.pop(vecino, None)
                    else:
                        continue

                if vecino not in g_cost or g_nuevo < g_cost[vecino]:
                    padres[vecino] = nodo
                    g_cost[vecino] = g_nuevo
                    f_nuevo = g_nuevo + self.heuristica(vecino)
                    abierta.push(vecino, f_nuevo, g_nuevo)

        tiempo_total = time.time() - inicio_t
        return None, None, expansiones, tiempo_total

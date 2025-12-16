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
        self.fin = fin

    def reconstruir_camino(self, padres, nodo_final):
        """
        Reconstruye el camino final desde el nodo inicial hasta el nodo_final.
        """
        camino = []
        actual = nodo_final

        # Vamos hacia atrás desde el final hasta llegar al inicio (padre None).
        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual)

        camino.reverse()
        return camino

    def heuristica(self, nodo):
        """
        Calcula la heurística para un nodo.
        En nuestro caso: distancia "en línea recta" hasta el objetivo (Haversine).
        IMPORTANTE: multiplicamos por 10 porque los costes del grafo están en decímetros.
        Restamos 1 como margen de seguridad para evitar sobrestimación por discretización.
        Truncamos (int) para no sobrestimar nunca.
        """
        return max(0, int(self.grafo.distancia(nodo, self.fin) * 10) - 1)

    # ------------------------------------------------------------
    # BÚSQUEDA GENÉRICA TIPO A*
    # La usamos para:
    # - Fuerza bruta: h(n)=0 (equivale a Dijkstra/UCS)
    # - A*: h(n)=distancia geográfica (entera)
    # ------------------------------------------------------------
    def buscar(self, funcion_h, abierta):
        """
        Búsqueda genérica estilo A*.
        Recibe:
        - funcion_h(n): heurística (si es 0 => fuerza bruta/Dijkstra)
        - abierta: estructura de abiertos (puede ser Abierta normal o Dial adaptado)
        """
        inicio_t = time.perf_counter()

        cerrada = Cerrada()               # Nodos ya expandidos
        padres = {self.inicio: None}      # Para reconstruir el camino
        g_cost = {self.inicio: 0}         # Mejor g conocido por nodo
        expansiones = 0

        # Metemos el inicio en abiertos.
        g_inicial = 0
        f_inicial = g_inicial + funcion_h(self.inicio)
        abierta.push(self.inicio, f_inicial, g_inicial)

        while True:
            extraido = abierta.pop()
            if extraido is None:
                break

            nodo, f_actual, g_actual = extraido

            # Si esta entrada no coincide con el mejor g que conocemos, es antigua.
            # ERROR COMÚN: al usar buckets por f, pueden salir nodos en orden correcto de f
            # pero con g antiguo. Verificamos g_cost.
            if g_actual != g_cost.get(nodo, None):
                continue

            # Si ya lo cerramos con un coste mejor o igual, lo ignoramos.
            if cerrada.contiene(nodo):
                if g_actual >= cerrada.coste(nodo):
                    continue
                # Si encontramos un camino mejor, lo reabrimos.
                cerrada.cerrados.pop(nodo, None)

            expansiones += 1

            # Si llegamos al objetivo, terminamos.
            if nodo == self.fin:
                camino = self.reconstruir_camino(padres, nodo)
                tiempo_total = time.perf_counter() - inicio_t
                return camino, g_actual, expansiones, tiempo_total

            # Cerramos el nodo (ya lo expandimos).
            cerrada.anadir(nodo, g_actual)

            # Probamos a mejorar a los vecinos.
            for vecino, coste_arco in self.grafo.vecinos(nodo):
                nuevo_g = g_actual + coste_arco

                # Si el vecino ya está cerrado con mejor o igual coste, no interesa.
                if cerrada.contiene(vecino) and nuevo_g >= cerrada.coste(vecino):
                    continue

                # Si es la primera vez o mejora, actualizamos.
                if vecino not in g_cost or nuevo_g < g_cost[vecino]:
                    g_cost[vecino] = nuevo_g
                    padres[vecino] = nodo
                    # h(n) debe ser entero
                    h_vecino = int(funcion_h(vecino))
                    nuevo_f = nuevo_g + h_vecino
                    
                    # En Dial modificado indexamos por F
                    abierta.push(vecino, nuevo_f, nuevo_g)

        tiempo_total = time.perf_counter() - inicio_t
        return None, None, expansiones, tiempo_total

    def fuerza_bruta(self):
        """
        Búsqueda por fuerza bruta (Dijkstra/UCS): h(n) = 0.
        Usa la misma estructura Abierta que A*, solo cambia la heurística.
        """
        abierta = Abierta()
        return self.buscar(lambda n: 0, abierta)

    def a_estrella(self):
        """
        Búsqueda A*: h(n) = distancia Haversine (entera, truncada).
        Usa la misma estructura Abierta que Dijkstra.
        """
        abierta = Abierta()
        return self.buscar(self.heuristica, abierta)

    def dijkstra(self):
        """
        Dijkstra = fuerza bruta = A* con h(n)=0.
        """
        return self.fuerza_bruta()

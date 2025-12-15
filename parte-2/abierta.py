import heapq


class Abierta:
    """
    Estructura de abiertos para A*.
    Guardamos nodos pendientes ordenados por f = g + h.
    """
    def __init__(self):
        """
        Inicializa la estructura 'Abierta'.
        """
        self.cola_prioridad = []   # Aquí se almacenan (f, g, nodo) ordenados por f
        self.mejor_g = {}          # Diccionario: nodo -> mejor g encontrado hasta ahora

    def push(self, nodo, coste_f, coste_g):
        """
        Inserta un nodo en abiertos si mejora el coste g.
        Si llega una versión peor, la ignoramos.
        """
        g_prev = self.mejor_g.get(nodo)

        # Solo guardamos esta versión si es la primera o si tiene un g mejor.
        if g_prev is None or coste_g < g_prev:
            self.mejor_g[nodo] = coste_g

            # Metemos la entrada. Si había una versión anterior peor, quedará por ahí,
            # pero luego se descartará al hacer pop.
            heapq.heappush(self.cola_prioridad, (coste_f, coste_g, nodo))

    def pop(self):
        """
        Extrae el nodo con menor f.
        Si encuentra entradas antiguas (obsoletas), las descarta y sigue buscando.
        """
        while self.cola_prioridad:
            coste_f, coste_g, nodo = heapq.heappop(self.cola_prioridad)

            # Esta entrada es válida si coincide con el mejor g actual de ese nodo.
            if self.mejor_g.get(nodo) == coste_g:
                return nodo, coste_f, coste_g

        # Si no hay nada válido, está vacío.
        return None

    def actualizar(self, nodo, nuevo_f, nuevo_g):
        """
        Actualizar es lo mismo que insertar (si mejora).
        """
        self.push(nodo, nuevo_f, nuevo_g)

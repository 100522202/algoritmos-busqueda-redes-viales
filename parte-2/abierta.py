import heapq


class Abierta:
    """
    Cola de prioridad basada en heap (min-heap).
    Esta versión es genérica y sirve perfectamente para A*:
    - coste_f = g + h
    - coste_g = g
    """
    def __init__(self):
        """
        Inicializa la estructura 'Abierta' asociada a los algoritmos de
        búsqueda (versión con heap).
        """
        self.cola_prioridad = []   # Cola de prioridad (min-heap)
        # Clave: nodo -> mejor tupla (f, g) registrada hasta ahora.
        self.guardados = {}

    def push(self, nodo, coste_f, coste_g):
        """
        Inserta un nodo en la cola de prioridad (heap).

        nodo     : identificador del nodo.
        coste_f  : valor usado para ordenar en la cola (f = g + h en A*).
        coste_g  : coste acumulado g(n).
        """
        guardado = self.guardados.get(nodo)  # Comprobamos si existe información previa del nodo.

        # Insertamos solo si no existe o si el coste f es mejor (más bajo).
        if guardado is None or coste_f < guardado[0]:
            # Actualizamos el mejor valor del nodo.
            self.guardados[nodo] = (coste_f, coste_g)
            # Añadimos al heap: se ordena por coste_f (después por coste_g).
            heapq.heappush(self.cola_prioridad, (coste_f, coste_g, nodo))

    def pop(self):
        """
        Extrae el nodo con menor coste_f de la cola de prioridad.

        Devuelve:
            (nodo, coste_f, coste_g)
        o None si la lista está vacía.
        """
        while self.cola_prioridad:
            # Sacamos el nodo con menor coste.
            coste_f, coste_g, nodo = heapq.heappop(self.cola_prioridad)

            # Comprobamos si los valores (f, g) coinciden con la versión actual guardada.
            if self.guardados.get(nodo) == (coste_f, coste_g):
                # Como el nodo es válido, lo eliminamos de guardados
                del self.guardados[nodo]

                # Y lo devolvemos porque es el correcto (entrada no obsoleta).
                return nodo, coste_f, coste_g

        # Si salimos del bucle, significa que no encontramos ninguna versión válida de ningún nodo.
        return None

    def actualizar(self, nodo, nuevo_f, nuevo_g):
        """
        Actualiza o inserta un nodo con nuevos valores (f, g).
        Es simplemente un alias de push, pero semánticamente más claro.
        """
        self.push(nodo, nuevo_f, nuevo_g)
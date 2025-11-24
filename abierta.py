import heapq


class Abierta:
    def __init__(self):
        """
        Inicializa la estructura 'Abierta' asociado a los algoritmos de
        búsqueda
        """
        self.cola_prioridad = []   # Cola de prioridad (min-heap)
        self.guardados = {}        # Clave:nodo -> mejor tupla (f, g) registrada hasta ahora.

    def push(self, nodo, coste_f, coste_g):
        """
        Inserta un nodo en la cola de prioridad
        """
        guardado = self.guardados.get(nodo)  # Comprobamos si existe información previa del nodo.

        # Insertamos solo si no existe o si el coste f es mejor (más bajo).
        if guardado is None or coste_f < guardado[0]:
            self.guardados[nodo] = (coste_f, coste_g)  # Actualizamos el mejor valor del nodo.
            heapq.heappush(self.cola_prioridad, (coste_f, coste_g, nodo))  # Añadimos al heap.

    def pop(self):
        """
        Extrae el nodo con menor coste_f de la cola de prioridad
        """
        while self.cola_prioridad:
            # Sacamos el nodo con menor coste
            coste_f, coste_g, nodo = heapq.heappop(self.cola_prioridad)

            # Comprobamos si los valores (f, g) coinciden con la versión actual guardada.
            if self.guardados.get(nodo) == (coste_f, coste_g):
                # Como el nodo es válido, lo eliminamos de guardados
                del self.guardados[nodo]

                # Y lo devolvemos porque es el correcto.
                return nodo, coste_f, coste_g

        # Si salimos del bucle, significa que no encontramos ninguna versión válida de ningún nodo.
        return None

    def actualizar(self, nodo, nuevo_f, nuevo_g):
        """
        Actualiza o inserta un nodo con nuevos valores
        """
        self.push(nodo, nuevo_f, nuevo_g)  # Se vuelve a insertar si mejora; si no, se ignora.

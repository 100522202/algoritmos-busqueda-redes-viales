class AbiertaDial:
    """
    Implementación de Dial's Bucket Queue para algoritmos SIN heurística
    (Dijkstra / Uniform Cost Search).

    Esta estructura asume:
      - Costes de los arcos enteros y positivos.
      - C_max es el coste máximo de un arco del grafo.

    Usa:
      - 'buckets': lista de listas, donde cada posición es un bucket.
      - 'actual' : coste mínimo candidato (el 'run min' del profesor).
      - 'guardados': nodo -> mejor g(n) conocido.

    Complejidad:
      - push: O(1) amortizado
      - pop : O(1) amortizado (a costa de escanear hasta C_max buckets).
    """
    def __init__(self, C_max):
        """
        C_max: coste máximo de un arco del grafo (entero > 0).
        """
        if C_max <= 0:
            raise ValueError("C_max debe ser un entero positivo mayor que 0.")

        self.C_max = C_max
        self.N = C_max + 1                 # número de buckets del anillo
        self.buckets = [[] for _ in range(self.N)]
        self.actual = 0                    # coste mínimo candidato (run-min)
        self.guardados = {}                # nodo -> mejor coste g conocido

    def push(self, nodo, coste_g):
        """
        Inserta o actualiza un nodo en la estructura Dial.

        nodo    : identificador del nodo.
        coste_g : coste acumulado g(n), entero y >= 0.
        """
        anterior = self.guardados.get(nodo)

        # Si ya tenemos un g mejor o igual para este nodo, ignoramos.
        if anterior is not None and coste_g >= anterior:
            return

        # Actualizamos el mejor g para este nodo.
        self.guardados[nodo] = coste_g

        # Calculamos el índice del bucket usando aritmética modular (anillo).
        indice = coste_g % self.N
        self.buckets[indice].append(nodo)

    def pop(self):
        """
        Extrae el nodo con menor coste_g disponible.

        Devuelve:
            (nodo, coste_g)
        o None si no queda ningún nodo pendiente.
        """
        # Si no hay ningún nodo registrado, la estructura está vacía.
        if not self.guardados:
            return None

        while True:
            # Índice del bucket correspondiente al coste 'actual'.
            indice = self.actual % self.N
            bucket = self.buckets[indice]

            # Mientras haya candidatos en este bucket...
            while bucket:
                nodo = bucket.pop()  # O(1) sacando del final

                # Obtenemos el mejor g conocido actualmente para este nodo.
                g_mejor = self.guardados.get(nodo)

                if g_mejor is None:
                    # Este nodo ya fue extraído antes con su mejor coste; copia obsoleta.
                    continue

                if g_mejor != self.actual:
                    # Esta entrada es obsoleta respecto al valor 'actual':
                    # el nodo tiene ahora un coste distinto (mayor) y será
                    # tratado cuando self.actual alcance ese nuevo valor.
                    continue

                # En este punto g_mejor == self.actual, y este nodo es el
                # siguiente con coste mínimo.
                del self.guardados[nodo]
                return nodo, g_mejor

            # Si este bucket está vacío (o sólo tenía entradas obsoletas),
            # avanzamos 'actual' al siguiente coste posible.
            self.actual += 1

            # Si ya no quedan nodos registrados, terminamos.
            if not self.guardados:
                return None

    def vacia(self):
        """
        Indica si no queda ningún nodo pendiente en la estructura.
        """
        return not self.guardados

class AbiertaDialAStar:
    """
    Adaptador para poder usar Dial como 'abierta' en el motor de A*.
    En fuerza bruta h=0, así que f=g.
    """

    def __init__(self, C_max):
        self.dial = AbiertaDial(C_max)

    def push(self, nodo, coste_f, coste_g):
        # Dial trabaja con g (entero). El f aquí no hace falta porque h=0.
        self.dial.push(nodo, int(coste_g))

    def pop(self):
        res = self.dial.pop()
        if res is None:
            return None
        nodo, g = res
        # Como h=0, f = g.
        return nodo, g, g


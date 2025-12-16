import heapq


class Abierta:
    """
    Estructura de abiertos única, con dos modos:
    - modo="heap": para A* (ordenamos por f = g + h)
    - modo="dial": para fuerza bruta (h=0 => f=g) usando listas por coste (Dial)
    """

    def __init__(self, modo="heap", C_max=None):
        self.modo = modo

        # --- Modo heap (A*) ---
        self.heap_abiertos = []     # (f, g, nodo)
        self.mejor_coste_g = {}     # nodo -> mejor g conocido

        # --- Modo dial (fuerza bruta) ---
        self.coste_max_arco = None
        self.num_listas_coste = None
        self.listas_coste = None    # listas_coste[i] guarda nodos con un cierto coste (en anillo)
        self.coste_actual = 0       # coste mínimo que estamos buscando ahora
        self.mejor_g_dial = {}      # nodo -> mejor g conocido

        if self.modo == "dial":
            if C_max is None or C_max <= 0:
                raise ValueError("Para modo='dial' necesitas C_max > 0.")

            self.coste_max_arco = int(C_max)
            self.num_listas_coste = self.coste_max_arco + 1
            self.listas_coste = [[] for _ in range(self.num_listas_coste)]
            self.coste_actual = 0
            self.mejor_g_dial = {}

    def push(self, nodo, coste_f, coste_g):
        if self.modo == "heap":
            g_anterior = self.mejor_coste_g.get(nodo)
            if g_anterior is None or coste_g < g_anterior:
                self.mejor_coste_g[nodo] = coste_g
                heapq.heappush(self.heap_abiertos, (coste_f, coste_g, nodo))
            return

        # --- modo dial ---
        coste_g = int(coste_g)
        g_anterior = self.mejor_g_dial.get(nodo)

        if g_anterior is not None and coste_g >= g_anterior:
            return

        self.mejor_g_dial[nodo] = coste_g

        # Metemos el nodo en la lista que le toca según su coste (usando anillo)
        indice_coste = coste_g % self.num_listas_coste
        self.listas_coste[indice_coste].append(nodo)

    def pop(self):
        if self.modo == "heap":
            while self.heap_abiertos:
                coste_f, coste_g, nodo = heapq.heappop(self.heap_abiertos)
                if self.mejor_coste_g.get(nodo) == coste_g:
                    return nodo, coste_f, coste_g
            return None

        # --- modo dial ---
        if not self.mejor_g_dial:
            return None

        while True:
            indice_coste = self.coste_actual % self.num_listas_coste
            lista_coste = self.listas_coste[indice_coste]

            while lista_coste:
                nodo = lista_coste.pop()
                g_registrado = self.mejor_g_dial.get(nodo)

                if g_registrado is None:
                    continue
                if g_registrado != self.coste_actual:
                    continue

                del self.mejor_g_dial[nodo]
                return nodo, g_registrado, g_registrado  # h=0 => f=g

            self.coste_actual += 1
            if not self.mejor_g_dial:
                return None

    def actualizar(self, nodo, nuevo_f, nuevo_g):
        self.push(nodo, nuevo_f, nuevo_g)

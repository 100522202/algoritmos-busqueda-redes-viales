import os  # Importamos 'os' para trabajar con archivos y comprobar si existen en el sistema.


class Grafo:
    def __init__(self, ruta_mapa):
        """
        Constructor del grafo
        """
        self.ruta_mapa = ruta_mapa           # Ruta base de los archivos
        self.coordenadas = {}                # Diccionario: clave:id_nodo contenido:(longitud, latitud)
        self.adyacencia = {}                 # Diccionario: id_nodo -> lista de (vecino, coste)
        self.num_vertices = 0                # Número total de vértices
        self.num_arcos = 0                   # Número total de arcos
        self.coste_maximo = 0                # Coste máximo encontrado en los arcos
        self.leer_coordenadas()              # Cargamos las coordenadas desde el archivo con extensión .co
        self.leer_grafo()                    # Cargamos los arcos desde el archivo con extensión .gr

    def _ruta(self, extension):
        """
        Construye y devuelve la ruta completa de un archivo
        """
        # Unimos la ruta base con la extensión
        return self.ruta_mapa + extension

    def leer_coordenadas(self):
        """
        Lee el archivo con extensión .co para obtener las coordenadas de cada vértice.
        """
        ruta = self._ruta(".co")  # Obtenemos la ruta completa del archivo de coordenadas.

        # Comprobamos que el archivo exista antes de intentar abrirlo.
        if not os.path.exists(ruta):
            # Si el archivo no existe, lanzamos un error claro para saber qué ha fallado.
            raise FileNotFoundError(f"No se encontro el fichero de coordenadas: {ruta}")

        # Abrimos el archivo en modo lectura de texto.
        with open(ruta, "r") as archivo:
            # Recorremos el archivo línea por línea.
            for linea in archivo:
                # Solo nos interesan las líneas que empiezan por "v ",
                # porque son las que definen vértices.
                if linea.startswith("v "):
                    # Dividimos la línea en partes usando el espacio como separador.
                    partes = linea.split()
                    identificador = int(partes[1])  # Convertimos el id a entero.
                    longitud = int(partes[2])        # Convertimos la longitud a entero.
                    latitud = int(partes[3])         # Convertimos la latitud a entero.
                    # Guardamos las coordenadas del vértice en el diccionario.
                    # La clave es el identificador del vértice y el valor es una tupla (longitud, latitud).
                    self.coordenadas[identificador] = (longitud, latitud)

        # El número de vértices es simplemente el tamaño del diccionario de coordenadas.
        self.num_vertices = len(self.coordenadas)

    def leer_grafo(self):
        """
        Lee el archivo con extensión .gr para construir la lista de adyacencia.
        """
        ruta = self._ruta(".gr")  # Obtenemos la ruta completa del archivo del grafo.

        # Verificamos que el archivo exista antes de abrirlo.
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontro el fichero de grafo: {ruta}")

        # Primero, inicializamos una lista vacía de vecinos para cada nodo conocido.
        # De esta forma, aunque un nodo no tenga arcos salientes, seguirá existiendo en la estructura.
        for nodo in self.coordenadas:
            self.adyacencia[nodo] = []  # Cada nodo empieza con una lista de adyacencia vacía.

        # Abrimos el archivo de grafo.
        with open(ruta, "r") as archivo:
            for linea in archivo:
                # Las líneas que definen arcos comienzan con "a ".
                if linea.startswith("a "):
                    partes = linea.split()
                    origen = int(partes[1])   # Nodo desde el que sale el arco.
                    destino = int(partes[2])  # Nodo al que llega el arco.
                    coste = int(partes[3])    # Coste o peso del arco.
                    # Añadimos el arco a la lista de adyacencia del nodo origen.
                    # Guardamos una tupla (destino, coste) para cada conexión.
                    self.adyacencia[origen].append((destino, coste))
                    # Incrementamos el contador de arcos cada vez que añadimos uno.
                    self.num_arcos += 1
                    # Actualizamos el coste máximo visto hasta ahora.
                    if coste > self.coste_maximo:
                        self.coste_maximo = coste

    def vecinos(self, nodo):
        """
        Devuelve la lista de vecinos del nodo indicado.
        """
        # Usamos .get para evitar errores si el nodo no está en el diccionario.
        # Si no se encuentra la clave 'nodo', se devuelve [] en lugar de dar un error.
        return self.adyacencia.get(nodo, [])

    def distancia(self, v1, v2):
        """
        Calcula y devuelve la distancia euclidiana entre dos vértices del grafo.
        """
        # Obtenemos las coordenadas del primer vértice.
        x1, y1 = self.coordenadas[v1]
        # Obtenemos las coordenadas del segundo vértice.
        x2, y2 = self.coordenadas[v2]
        # Calculamos la diferencia en X y en Y.
        dx = x1 - x2
        dy = y1 - y2
        # Aplicamos la fórmula de la distancia euclidiana.
        distancia = (dx * dx + dy * dy) ** 0.5
        return distancia

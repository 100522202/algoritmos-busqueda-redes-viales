import os  # Importamos 'os' para trabajar con archivos y comprobar si existen en el sistema.
import math

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
                    lon_micro = int(partes[2])
                    lat_micro = int(partes[3])
                    lon = lon_micro / 1_000_000.0
                    lat = lat_micro / 1_000_000.0
                    # Guardamos en radianes y en orden (lat, lon)
                    self.coordenadas[identificador] = (math.radians(lat),math.radians(lon))

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
                    self.adyacencia.setdefault(origen, []).append((destino, coste))
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
        Distancia Haversine entre v1 y v2 en metros.
        Las coordenadas se guardan en self.coordenadas como (lat_rad, lon_rad).
        """
        # Sacamos (latitud, longitud) en RADIANES de cada vértice.
        lat1, lon1 = self.coordenadas[v1]
        lat2, lon2 = self.coordenadas[v2]
        # Calculamos las diferencias de latitud y longitud.
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # Fórmula de Haversine:
        # Sirve para medir la distancia "en línea recta" sobre la superficie de la Tierra.
        # (como si fuéramos por el aire, no por carretera).
        a = (math.sin(dlat / 2) ** 2 +math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        # Convertimos el valor 'a' en un ángulo (en radianes).
        c = 2 * math.asin(math.sqrt(a))
        # Radio medio de la Tierra en metros.
        R = 6_371_000
        # Distancia final en metros.
        return R * c



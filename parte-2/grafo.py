# Este fichero contiene la clase Grafo que se encarga de:
# 1. Leer los ficheros .co (coordenadas) y .gr (arcos)
# 2. Guardar toda esa informacion en memoria
# 3. Calcular distancias entre nodos (formula de Haversine)
#
# Los ficheros vienen del 9th DIMACS Challenge y tienen un formato especifico.


import os    # Para comprobar si los ficheros existen
import math  # Para las funciones trigonometricas (seno, coseno, etc.)


class Grafo:
    """
    Clase que representa un grafo (mapa de carreteras).
    
    Lee los datos de dos ficheros:
    - .co: coordenadas (longitud y latitud de cada nodo)
    - .gr: grafo (arcos entre nodos con sus costes/distancias)
    
    Los nodos se identifican por numeros enteros (1, 2, 3, ...).
    """
    
    def __init__(self, ruta_mapa):
        """
        Constructor: carga el grafo desde los ficheros.
        
        Parametros:
            ruta_mapa: ruta base de los ficheros (sin extension)
                       Por ejemplo: "USA-road-d.BAY" buscara
                       "USA-road-d.BAY.co" y "USA-road-d.BAY.gr"
        """
        # Guardamos la ruta base
        self.ruta_mapa = ruta_mapa
        
        # Diccionario de coordenadas: nodo -> (latitud_rad, longitud_rad)
        # Guardamos las coordenadas en radianes para calcular distancias
        self.coordenadas = {}
        
        # Diccionario de adyacencia: nodo -> lista de (vecino, coste)
        # Para cada nodo, guardamos a que nodos podemos ir y cuanto cuesta
        self.adyacencia = {}
        
        # Estadisticas del grafo
        self.num_vertices = 0   # Cuantos nodos tiene
        self.num_arcos = 0      # Cuantas conexiones tiene
        self.coste_maximo = 0   # El arco mas caro (para Dial's algorithm)
        
        # Cargamos los datos de los ficheros
        self.leer_coordenadas()  # Primero las coordenadas (.co)
        self.leer_grafo()        # Luego los arcos (.gr)
    
    
    def _ruta(self, extension):
        """
        Construye la ruta completa de un fichero anadiendo la extension.
        
        Ejemplo: si ruta_mapa es "USA-road-d.BAY" y extension es ".co",
        devuelve "USA-road-d.BAY.co"
        """
        ruta_completa = self.ruta_mapa + extension
        return ruta_completa
    
    
    def leer_coordenadas(self):
        """
        Lee el fichero .co y carga las coordenadas de cada nodo.
        
        El formato del fichero es:
        - Lineas que empiezan por "c" son comentarios (las ignoramos)
        - Lineas que empiezan por "p" son cabeceras (las ignoramos)
        - Lineas que empiezan por "v" son vertices:
          v <id> <longitud*10^6> <latitud*10^6>
        
        Las coordenadas vienen multiplicadas por 10^6 para evitar decimales,
        asi que tenemos que dividir para obtener grados.
        """
        ruta = self._ruta(".co")
        
        # Comprobamos que el fichero existe
        if not os.path.exists(ruta):
            mensaje = f"No se encontro el fichero de coordenadas: {ruta}"
            raise FileNotFoundError(mensaje)
        
        # Abrimos el fichero para leer
        fichero = open(ruta, "r")
        
        # Leemos linea por linea
        for linea in fichero:
            # Solo nos interesan las lineas que empiezan por "v "
            if not linea.startswith("v "):
                continue
            
            # Separamos la linea por espacios
            partes = linea.split()
            
            # Sacamos los datos: v <id> <lon> <lat>
            id_nodo = int(partes[1])
            longitud_micro = int(partes[2])  # Longitud * 10^6
            latitud_micro = int(partes[3])   # Latitud * 10^6
            
            # Pasamos a grados (dividimos por 10^6)
            longitud_grados = longitud_micro / 1000000.0
            latitud_grados = latitud_micro / 1000000.0
            
            # Pasamos a radianes (necesario para la formula de Haversine)
            latitud_rad = math.radians(latitud_grados)
            longitud_rad = math.radians(longitud_grados)
            
            # Guardamos en el diccionario (latitud primero, luego longitud)
            self.coordenadas[id_nodo] = (latitud_rad, longitud_rad)
        
        fichero.close()
        
        # Contamos cuantos nodos hemos cargado
        self.num_vertices = len(self.coordenadas)
    
    
    def leer_grafo(self):
        """
        Lee el fichero .gr y carga los arcos del grafo.
        
        El formato del fichero es:
        - Lineas que empiezan por "c" son comentarios (las ignoramos)
        - Lineas que empiezan por "p" son cabeceras (las ignoramos)
        - Lineas que empiezan por "a" son arcos:
          a <origen> <destino> <coste>
        
        El coste esta en decimetros (segun descubrimos mirando el ratio).
        """
        ruta = self._ruta(".gr")
        
        # Comprobamos que el fichero existe
        if not os.path.exists(ruta):
            mensaje = f"No se encontro el fichero de grafo: {ruta}"
            raise FileNotFoundError(mensaje)
        
        # Inicializamos la lista de vecinos vacia para cada nodo
        # (asi aunque un nodo no tenga arcos salientes, seguira existiendo)
        for nodo in self.coordenadas:
            self.adyacencia[nodo] = []
        
        # Abrimos el fichero para leer
        fichero = open(ruta, "r")
        
        # Leemos linea por linea
        for linea in fichero:
            # Solo nos interesan las lineas que empiezan por "a "
            if not linea.startswith("a "):
                continue
            
            # Separamos la linea por espacios
            partes = linea.split()
            
            # Sacamos los datos: a <origen> <destino> <coste>
            origen = int(partes[1])
            destino = int(partes[2])
            coste = int(partes[3])
            
            # Anadimos el arco a la lista de adyacencia
            # Si el origen no existia (raro pero por si acaso), lo creamos
            if origen not in self.adyacencia:
                self.adyacencia[origen] = []
            
            # Guardamos la tupla (destino, coste)
            arco = (destino, coste)
            self.adyacencia[origen].append(arco)
            
            # Contamos este arco
            self.num_arcos = self.num_arcos + 1
            
            # Actualizamos el coste maximo si este es mayor
            if coste > self.coste_maximo:
                self.coste_maximo = coste
        
        fichero.close()
    
    
    def vecinos(self, nodo):
        """
        Devuelve la lista de vecinos de un nodo.
        
        Cada vecino es una tupla (nodo_vecino, coste_arco).
        Si el nodo no existe, devuelve lista vacia.
        """
        # Usamos .get() para no dar error si el nodo no existe
        lista = self.adyacencia.get(nodo, [])
        return lista
    
    
    def distancia(self, nodo1, nodo2):
        """
        Calcula la distancia en linea recta entre dos nodos.
        
        Usamos la formula de Haversine, que sirve para calcular
        la distancia mas corta entre dos puntos sobre una esfera
        (en este caso, la Tierra).
        
        Devuelve:
            La distancia en METROS.
        """
        # Sacamos las coordenadas de cada nodo (en radianes)
        lat1, lon1 = self.coordenadas[nodo1]
        lat2, lon2 = self.coordenadas[nodo2]
        
        # Calculamos las diferencias
        diferencia_lat = lat2 - lat1
        diferencia_lon = lon2 - lon1
        
        # Formula de Haversine (un poco lio, pero funciona)
        # Esto calcula la distancia sobre la superficie de la Tierra
        
        # Paso 1: calculamos 'a' (un valor intermedio)
        sin_lat = math.sin(diferencia_lat / 2)
        sin_lon = math.sin(diferencia_lon / 2)
        cos_lat1 = math.cos(lat1)
        cos_lat2 = math.cos(lat2)
        
        a = sin_lat * sin_lat + cos_lat1 * cos_lat2 * sin_lon * sin_lon
        
        # Paso 2: calculamos 'c' (el angulo central)
        c = 2 * math.asin(math.sqrt(a))
        
        # Paso 3: multiplicamos por el radio de la Tierra en metros
        # El radio medio de la Tierra es aproximadamente 6,371 km
        RADIO_TIERRA_METROS = 6371000
        
        distancia_metros = RADIO_TIERRA_METROS * c
        
        return distancia_metros

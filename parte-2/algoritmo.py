# =============================================================================
# ALGORITMO - Implementacion de A* y Dijkstra para buscar caminos
#
# Este fichero contiene la clase Algoritmo que sabe buscar el camino
# mas corto entre dos nodos de un grafo.
#
# Tenemos dos algoritmos:
#   - Dijkstra (fuerza bruta): explora todo sin usar heuristica
#   - A*: usa una heuristica para ir "hacia el destino" y ser mas rapido
# =============================================================================

import time  # Para medir cuanto tarda en encontrar el camino

# Importamos nuestras estructuras de datos
from abierta import Abierta   # Lista de nodos pendientes de explorar
from cerrada import Cerrada   # Lista de nodos ya explorados


class Algoritmo:
    """
    Clase que implementa los algoritmos de busqueda A* y Dijkstra.
    
    Ambos algoritmos son muy parecidos, la unica diferencia es que A*
    usa una heuristica (estimacion de distancia al destino) para decidir
    que nodos explorar primero, mientras que Dijkstra no usa ninguna
    (es como si la heuristica fuera siempre 0).
    """
    
    def __init__(self, grafo, inicio, fin):
        """
        Constructor: guarda el grafo y los nodos de inicio y fin.
        
        Parametros:
            grafo: el grafo con los nodos y arcos (lo cargamos de los ficheros)
            inicio: el nodo desde donde empezamos a buscar
            fin: el nodo al que queremos llegar
        """
        self.grafo = grafo
        self.inicio = inicio
        self.fin = fin
    
    
    def reconstruir_camino(self, padres, nodo_final):
        """
        Una vez encontrado el destino, reconstruye el camino completo.
        
        Durante la busqueda vamos guardando de donde venimos (el "padre" de cada nodo).
        Esta funcion va hacia atras desde el destino hasta el inicio
        siguiendo esos padres, y nos da el camino completo.
        
        Por ejemplo si los padres son: {309: 308, 308: 1, 1: None}
        El camino seria: [1, 308, 309]
        """
        camino = []
        nodo_actual = nodo_final
        
        # Vamos hacia atras hasta llegar al inicio (que tiene padre None)
        while nodo_actual is not None:
            camino.append(nodo_actual)
            nodo_actual = padres.get(nodo_actual)
        
        # El camino esta al reves (del final al inicio), asi que le damos la vuelta
        camino.reverse()
        
        return camino
    
    
    def heuristica(self, nodo):
        """
        Calcula la heuristica h(n) para un nodo.
        
        La heuristica es una ESTIMACION de cuanto nos queda para llegar al destino.
        Usamos la distancia "en linea recta" (formula de Haversine) porque
        es la menor distancia posible entre dos puntos de la Tierra.
        
        IMPORTANTE: 
        - Multiplicamos por 9.8 (no 10) porque aunque los costes nominales son
          en decimetros, hay cierta variacion en los datos (ratio ≈ 9.99).
        - Esto asegura que la heuristica sea ADMISIBLE (nunca sobrestima).
          Si sobrestimamos, A* encontraria caminos suboptimos.
        - Usamos int() para truncar (redondear hacia abajo).
        - Factor 9.8 da margen de 2%: seguro en todas las distancias.
        
        Esta heuristica es ADMISIBLE porque nunca sobrestima el coste real.
        """
        # Calculamos la distancia en linea recta (en metros)
        distancia_metros = self.grafo.distancia(nodo, self.fin)
        
        # Pasamos a decimetros con factor conservador (9.8 en vez de 10)
        distancia_decimetros = distancia_metros * 9.8
        
        # Truncamos a entero (redondea hacia abajo)
        heuristica_final = int(distancia_decimetros)
        
        # Nos aseguramos de que nunca sea negativa
        if heuristica_final < 0:
            heuristica_final = 0
        
        return heuristica_final
    
    
    def buscar(self, funcion_h, abierta):
        """
        Algoritmo de busqueda generico (funciona para A* y Dijkstra).
        
        La idea es muy sencilla:
        1. Empezamos en el nodo inicio
        2. Miramos todos sus vecinos y los metemos en la lista "abierta"
        3. Sacamos el mejor nodo de abierta (el que tenga menor f = g + h)
        4. Si es el destino, hemos terminado
        5. Si no, miramos sus vecinos y repetimos desde el paso 3
        
        Parametros:
            funcion_h: la funcion heuristica (si es 0, es Dijkstra)
            abierta: la estructura para guardar los nodos pendientes
        
        Devuelve:
            (camino, coste, expansiones, tiempo)
            - camino: lista de nodos del inicio al fin
            - coste: coste total del camino
            - expansiones: cuantos nodos hemos explorado
            - tiempo: cuanto ha tardado en segundos
        """
        # Empezamos a medir el tiempo
        tiempo_inicio = time.perf_counter()
        
        # Lista cerrada: nodos que ya hemos explorado completamente
        cerrada = Cerrada()
        
        # Diccionario de padres: para cada nodo, guardamos de donde venimos
        # El nodo inicio no tiene padre (viene de None)
        padres = {}
        padres[self.inicio] = None
        
        # Diccionario de costes g: el mejor coste conocido para llegar a cada nodo
        # Al inicio, el coste para llegar al nodo inicio es 0
        g_costes = {}
        g_costes[self.inicio] = 0
        
        # Contador de cuantos nodos hemos expandido (para estadisticas)
        expansiones = 0
        
        # Calculamos f inicial = g + h para el nodo inicio
        g_inicio = 0
        h_inicio = funcion_h(self.inicio)
        f_inicio = g_inicio + h_inicio
        
        # Metemos el nodo inicio en la lista abierta
        abierta.push(self.inicio, f_inicio, g_inicio)
        
        # Bucle principal: seguimos mientras queden nodos por explorar
        while True:
            # Sacamos el nodo con menor f de la lista abierta
            resultado = abierta.pop()
            
            # Si no hay mas nodos, no encontramos camino
            if resultado is None:
                break
            
            # Desempaquetamos el resultado
            nodo = resultado[0]
            f_nodo = resultado[1]
            g_nodo = resultado[2]
            
            # Comprobacion importante: puede que este nodo ya no sea valido
            # (porque encontramos un camino mejor despues de meterlo en abierta)
            g_guardado = g_costes.get(nodo)
            if g_guardado is not None and g_nodo != g_guardado:
                # Este nodo tiene un g antiguo, lo ignoramos
                continue
            
            # Si ya lo cerramos antes con mejor coste, lo ignoramos
            if cerrada.contiene(nodo):
                coste_cerrado = cerrada.coste(nodo)
                if g_nodo >= coste_cerrado:
                    continue
            
            # Comprobamos si hemos llegado al destino
            if nodo == self.fin:
                # Reconstruimos el camino y devolvemos
                camino = self.reconstruir_camino(padres, nodo)
                tiempo_total = time.perf_counter() - tiempo_inicio
                return (camino, g_nodo, expansiones, tiempo_total)
            # Ahora sí: este nodo lo vamos a expandir de verdad
            expansiones = expansiones + 1
            
            # Cerramos este nodo (ya lo hemos explorado)
            cerrada.anadir(nodo, g_nodo)
            
            # Miramos todos los vecinos de este nodo
            lista_vecinos = self.grafo.vecinos(nodo)
            
            for vecino, coste_arco in lista_vecinos:
                # Calculamos el nuevo coste g para llegar al vecino
                nuevo_g = g_nodo + coste_arco
                
                # Si el vecino ya esta cerrado con mejor coste, lo saltamos
                if cerrada.contiene(vecino):
                    coste_cerrado = cerrada.coste(vecino)
                    if nuevo_g >= coste_cerrado:
                        continue
                
                # Miramos si ya conocemos un camino mejor a este vecino
                g_anterior = g_costes.get(vecino)
                
                if g_anterior is None or nuevo_g < g_anterior:
                    # Este camino es mejor, lo actualizamos
                    g_costes[vecino] = nuevo_g
                    padres[vecino] = nodo
                    
                    # Calculamos h y f para el vecino
                    h_vecino = funcion_h(vecino)
                    h_vecino = int(h_vecino)  # Por si acaso, lo pasamos a entero
                    f_vecino = nuevo_g + h_vecino
                    
                    # Lo metemos en la lista abierta
                    abierta.push(vecino, f_vecino, nuevo_g)
        
        # Si llegamos aqui, no encontramos camino
        tiempo_total = time.perf_counter() - tiempo_inicio
        return (None, None, expansiones, tiempo_total)
    
    
    def fuerza_bruta(self):
        """
        Busqueda por fuerza bruta (Dijkstra).
        
        Es exactamente igual que A* pero con heuristica = 0.
        Esto hace que explore los nodos solo por su coste g,
        sin tener en cuenta la distancia al destino.
        
        Es mas lento que A* porque explora mas nodos, pero
        siempre encuentra el camino optimo.
        """
        # Creamos la lista abierta (necesita el coste maximo del grafo)
        coste_max = self.grafo.coste_maximo
        abierta = Abierta(coste_max)
        
        # Usamos una funcion que siempre devuelve 0 como heuristica
        def heuristica_cero(nodo):
            return 0
        
        # Llamamos a buscar con esa heuristica
        return self.buscar(heuristica_cero, abierta)
    
    
    def a_estrella(self):
        """
        Busqueda A* (A estrella).
        
        Usa una heuristica para estimar cuanto queda hasta el destino.
        Gracias a esto, explora primero los nodos que "parecen" mas
        prometedores, y encuentra el camino mucho mas rapido.
        
        Si la heuristica es admisible (nunca sobrestima), A* siempre
        encuentra el camino optimo igual que Dijkstra, pero mas rapido.
        """
        # Creamos la lista abierta (necesita el coste maximo del grafo)
        coste_max = self.grafo.coste_maximo
        abierta = Abierta(coste_max)
        
        # Llamamos a buscar con nuestra heuristica (distancia Haversine)
        return self.buscar(self.heuristica, abierta)
    
    
    def dijkstra(self):
        """
        Alias para fuerza_bruta (son lo mismo).
        
        Dijkstra es el nombre del algoritmo, fuerza_bruta es como
        lo llamamos nosotros para comparar con A*.
        """
        return self.fuerza_bruta()

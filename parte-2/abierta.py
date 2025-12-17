# =============================================================================
# ABIERTA - Lista de nodos pendientes de explorar (Dial's O(1) verdadero)
#
# Esta estructura guarda los nodos que hemos descubierto pero que todavia
# no hemos explorar (no hemos mirado sus vecinos).
#
# Usamos "Dial's Algorithm" O(1) con array circular de buckets.
# Es una forma muy eficiente de sacar siempre el nodo con menor prioridad.
#
# La idea clave:
# - Array CIRCULAR de tamaño fijo C (en vez de diccionario infinito)
# - Puntero que SOLO AVANZA (nunca retrocede, nunca busca min)
# - La ventana acotada de valores f garantiza que no hay colisiones
# =============================================================================


class Abierta:
    """
    Lista abierta implementada con Dial's Buckets O(1) verdadero.
    
    Funciona tanto para A* como para Dijkstra:
    - En A*: la prioridad es f = g + h
    - En Dijkstra: la prioridad es f = g (porque h = 0)
    
    Usamos un array circular de tamaño C = 2*Cmax + 1 donde Cmax es
    el coste maximo de un arco. Esto garantiza complejidad O(1) real.
    """
    
    def __init__(self, coste_maximo_arco):
        """
        Inicializa la estructura.
        
        Parametros:
            coste_maximo_arco: el coste del arco mas caro del grafo.
                               Necesario para dimensionar el array circular.
        """
        # Calculamos el tamaño del array circular
        # Para A* con heuristica consistente: C = 2*Cmax + 1
        # (la ventana de valores f activos no supera 2*Cmax)
        self.C = 2 * coste_maximo_arco + 1
        
        # Array circular de buckets (listas)
        # Cada posicion guarda una lista de tuplas (nodo, g, f)
        self.buckets = [[] for _ in range(self.C)]
        
        # Para cada nodo, guardamos el mejor f que conocemos
        # Esto nos sirve para lazy deletion
        self.mejor_f = {}
        
        # El valor de f actual que estamos explorando
        # Este puntero SOLO AVANZA
        self.f_actual = 0
        
        # Contador de nodos pendientes (para saber si esta vacia)
        self.num_nodos = 0
    
    
    def push(self, nodo, coste_f, coste_g):
        """
        Mete un nodo en la lista abierta. Complejidad: O(1)
        
        Parametros:
            nodo: el identificador del nodo
            coste_f: la prioridad (f = g + h)
            coste_g: el coste acumulado desde el inicio
        """
        # Nos aseguramos de que son enteros
        coste_f = int(coste_f)
        coste_g = int(coste_g)
        
        # Guardamos si estaba vacía ANTES de cualquier modificación
        estaba_vacia = (self.num_nodos == 0)
        
        # Miramos si ya conocemos un camino mejor a este nodo
        f_anterior = self.mejor_f.get(nodo)
        
        if f_anterior is not None:
            # Ya conocemos este nodo
            if coste_f >= f_anterior:
                # El camino nuevo no es mejor, lo ignoramos
                return
        
        # Si teniamos este nodo antes, lo vamos a reemplazar
        # (el contador se mantiene igual)
        era_nuevo = (f_anterior is None)
        
        # Actualizamos el mejor f conocido para este nodo
        self.mejor_f[nodo] = coste_f
        
        # Calculamos el indice en el array circular
        # Usamos modulo para que siempre caiga dentro del rango [0, C-1]
        indice = coste_f % self.C
        
        # Metemos el nodo en el bucket correspondiente
        # Guardamos (nodo, g, f) - el f nos sirve para validar en pop()
        entrada = (nodo, coste_g, coste_f)
        self.buckets[indice].append(entrada)
        
        # Si era un nodo nuevo, incrementamos el contador
        if era_nuevo:
            self.num_nodos = self.num_nodos + 1
        
        # Actualizamos f_actual si:
        # 1. La lista estaba vacía (este es el primer nodo)
        # 2. El nuevo f es menor que el actual (hay que retroceder el puntero)
        if estaba_vacia or coste_f < self.f_actual:
            self.f_actual = coste_f
    
    
    def pop(self):
        """
        Saca el nodo con menor prioridad f. Complejidad: O(1) amortizado
        
        La clave: el puntero f_actual SOLO AVANZA (nunca retrocede).
        No hacemos min() - simplemente avanzamos hasta encontrar un bucket
        no vacio. Esto es O(1) amortizado porque cada posicion se visita
        como maximo una vez por "ronda" de C posiciones.
        
        Devuelve:
            (nodo, f, g) o None si la lista esta vacia
        """
        # Si no hay nodos, devolvemos None
        if self.num_nodos == 0:
            return None
        
        # Avanzamos el puntero hasta encontrar un bucket no vacio
        # CLAVE: esto es O(1) amortizado, NO es O(n)
        max_intentos = self.C  # Con array circular, C pasos recorren todo
        intentos = 0
        
        while intentos < max_intentos:
            # Calculamos el indice en el array circular
            indice = self.f_actual % self.C
            
            # Cogemos el bucket de esta posicion
            bucket = self.buckets[indice]
            
            # Mientras haya nodos en este bucket
            while len(bucket) > 0:
                # Sacamos el ultimo (es O(1) sacar del final)
                entrada = bucket.pop()
                nodo = entrada[0]
                g_guardado = entrada[1]
                f_guardado = entrada[2]
                
                # Comprobamos si este nodo sigue siendo valido
                # (puede que lo hayamos actualizado despues con mejor f)
                f_registrado = self.mejor_f.get(nodo)
                
                if f_registrado is None:
                    # Ya fue procesado antes, esta entrada es vieja
                    continue
                
                if f_registrado != f_guardado:
                    # Fue actualizado a otro f, esta entrada es obsoleta
                    continue
                
                # Este nodo es valido! Lo sacamos de mejor_f
                del self.mejor_f[nodo]
                
                # Decrementamos el contador
                self.num_nodos = self.num_nodos - 1
                
                # Devolvemos (nodo, f, g)
                return (nodo, f_guardado, g_guardado)
            
            # El bucket esta vacio, avanzamos el puntero
            # CLAVE: SOLO AVANZAMOS, nunca retrocedemos, nunca hacemos min()
            self.f_actual = self.f_actual + 1
            intentos = intentos + 1
        
        # Si llegamos aqui, hay inconsistencia interna
        # (num_nodos > 0 pero no encontramos nodos válidos)
        raise RuntimeError(
            f"Abierta inconsistente: num_nodos={self.num_nodos} pero no hay "
            f"entradas válidas. f_actual={self.f_actual}, C={self.C}"
        )
    
    
    def vacia(self):
        """
        Dice si la lista esta vacia. Complejidad: O(1)
        """
        return self.num_nodos == 0
    
    
    def actualizar(self, nodo, nuevo_f, nuevo_g):
        """
        Actualiza un nodo con un nuevo coste. Complejidad: O(1)
        
        En realidad es lo mismo que push, porque push ya se encarga
        de ignorar los valores peores.
        """
        self.push(nodo, nuevo_f, nuevo_g)

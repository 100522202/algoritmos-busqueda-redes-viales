from collections import defaultdict


class Abierta:
    """
    Implementación de lista abierta usando Dial's Buckets con diccionario dinámico.
    
    Funciona tanto para A* como para Dijkstra:
    - A*: f = g + h (donde h es la heurística truncada a entero)
    - Dijkstra: f = g (equivalente a h = 0)
    
    Al usar un defaultdict, evitamos colisiones por aritmética modular.
    Los buckets se crean dinámicamente según los valores de f.
    """

    def __init__(self):
        # Buckets indexados por f (prioridad). Cada bucket es una lista de (nodo, g).
        self.buckets = defaultdict(list)
        
        # Para lazy deletion: nodo -> mejor f conocido
        self.mejor_f = {}
        
        # Prioridad actual (el f mínimo que estamos explorando)
        self.f_actual = 0

    def push(self, nodo, coste_f, coste_g):
        """
        Inserta un nodo con prioridad f y coste acumulado g.
        
        coste_f y coste_g deben ser enteros (ya convertidos).
        """
        coste_f = int(coste_f)
        coste_g = int(coste_g)
        
        # Si ya conocemos un camino con f menor o igual, descartamos
        f_anterior = self.mejor_f.get(nodo)
        if f_anterior is not None and coste_f >= f_anterior:
            return
        
        # Actualizamos el mejor f conocido para este nodo
        self.mejor_f[nodo] = coste_f
        
        # Insertamos en el bucket correspondiente a f
        self.buckets[coste_f].append((nodo, coste_g))
        
        # Si insertamos algo con f menor que f_actual, actualizamos
        if coste_f < self.f_actual:
            self.f_actual = coste_f

    def pop(self):
        """
        Extrae el nodo con menor f.
        
        Devuelve (nodo, f, g) o None si está vacía.
        """
        if not self.mejor_f:
            return None
        
        while True:
            # Obtener el bucket del f_actual
            bucket = self.buckets[self.f_actual]
            
            while bucket:
                nodo, g_insertado = bucket.pop()
                
                # Verificar si esta entrada sigue siendo válida
                f_registrado = self.mejor_f.get(nodo)
                
                if f_registrado is None:
                    # Ya fue procesado, entrada obsoleta
                    continue
                
                if f_registrado != self.f_actual:
                    # Fue actualizado a un f diferente, entrada obsoleta
                    continue
                
                # Este nodo es válido, lo extraemos
                del self.mejor_f[nodo]
                return nodo, self.f_actual, g_insertado
            
            # Bucket vacío, limpiamos y buscamos el siguiente f mínimo
            if self.f_actual in self.buckets:
                del self.buckets[self.f_actual]
            
            # Si no quedan nodos, terminamos
            if not self.mejor_f:
                return None
            
            # Saltar al siguiente f mínimo que tenga nodos
            # Buscamos el mínimo f que aún está en mejor_f
            self.f_actual = min(self.mejor_f.values())

    def vacia(self):
        """Indica si no quedan nodos pendientes."""
        return not self.mejor_f

    def actualizar(self, nodo, nuevo_f, nuevo_g):
        """Actualiza un nodo (equivale a push con lazy deletion)."""
        self.push(nodo, nuevo_f, nuevo_g)

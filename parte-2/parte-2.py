# Este es el programa que ejecutamos desde la terminal.
# Recibe 4 argumentos: nodo origen, nodo destino, nombre del mapa y fichero salida.
# Luego carga el grafo, busca el camino optimo y lo guarda en un fichero.

import sys   # Para leer los argumentos de la linea de comandos
import os    # Para manejar rutas de ficheros

# Importamos nuestras clases que hemos creado en otros ficheros
from grafo import Grafo
from algoritmo import Algoritmo


def normalizar_ruta(nombre):
    """
    Esta funcion sirve para arreglar las rutas de los ficheros.
    
    El problema es que a veces el usuario pone solo el nombre del fichero
    (por ejemplo "mapa") y otras veces pone la ruta completa 
    (por ejemplo "C:/mapas/mapa").
    
    Si solo pone el nombre, asumimos que el fichero esta en la misma
    carpeta que este script de Python.
    """
    # Miramos si el nombre tiene alguna ruta (barras / o \)
    tiene_ruta = os.path.dirname(nombre)
    
    if tiene_ruta:
        # Si ya tiene ruta, lo dejamos como esta
        return nombre
    
    # Si no tiene ruta, le ponemos la carpeta donde esta este script
    carpeta_script = os.path.dirname(os.path.realpath(__file__))
    ruta_completa = os.path.join(carpeta_script, nombre)
    
    return ruta_completa


def escribir_camino(grafo, camino, fichero_salida):
    """
    Escribe el camino encontrado en un fichero con el formato que pide el enunciado:
    1 - (coste) - 308 - (coste) - 309
    
    Basicamente vamos poniendo cada nodo y entre medias el coste del arco.
    """
    # Si no hay camino, no escribimos nada
    if not camino:
        return

    # Abrimos el fichero para escribir
    fichero = open(fichero_salida, "w")
    
    # Escribimos el primer nodo del camino
    primer_nodo = camino[0]
    fichero.write(str(primer_nodo))

    # Ahora vamos recorriendo el camino de 2 en 2 nodos consecutivos
    # Por ejemplo si el camino es [1, 308, 309], miramos (1,308) y luego (308,309)
    for i in range(len(camino) - 1):
        nodo_actual = camino[i]
        nodo_siguiente = camino[i + 1]
        
        # Tenemos que buscar el coste del arco entre estos dos nodos
        # Para eso miramos los vecinos del nodo actual
        coste_arco = None
        lista_vecinos = grafo.vecinos(nodo_actual)
        
        for vecino, coste in lista_vecinos:
            if vecino == nodo_siguiente:
                coste_arco = coste
                break  # Ya lo encontramos, salimos del bucle
        
        # Si no encontramos el arco, algo ha ido mal
        if coste_arco is None:
            fichero.close()
            mensaje_error = f"Error: no existe arco de {nodo_actual} a {nodo_siguiente}"
            raise ValueError(mensaje_error)
        
        # Escribimos el formato: - (coste) - nodo
        texto = f" - ({coste_arco}) - {nodo_siguiente}"
        fichero.write(texto)

    # Ponemos un salto de linea al final y cerramos
    fichero.write("\n")
    fichero.close()


def main():
    """
    Funcion principal del programa.
    Aqui es donde pasa todo: leemos argumentos, cargamos el grafo,
    ejecutamos el algoritmo y guardamos el resultado.
    """
    
    # Primero comprobamos que nos han pasado los 4 argumentos necesarios
    # sys.argv[0] es el nombre del script, asi que en total son 5
    numero_argumentos = len(sys.argv)
    
    if numero_argumentos != 5:
        print("Uso: parte-2.py vertice-1 vertice-2 nombre-del-mapa fichero-salida")
        print("Ejemplo: python parte-2.py 1 309 USA-road-d.BAY solucion.txt")
        sys.exit(1)  # Salimos con codigo de error

    # Leemos los argumentos uno por uno
    origen = int(sys.argv[1])          # Nodo de inicio (lo pasamos a entero)
    destino = int(sys.argv[2])         # Nodo al que queremos llegar
    nombre_mapa = sys.argv[3]          # Nombre base de los ficheros del mapa
    fichero_salida = sys.argv[4]       # Donde guardaremos el resultado

    # Arreglamos las rutas por si el usuario no puso la ruta completa
    ruta_mapa = normalizar_ruta(nombre_mapa)
    fichero_salida = normalizar_ruta(fichero_salida)

    # =========================================================================
    # PASO 1: Cargar el grafo desde los ficheros
    # =========================================================================
    print("Leyendo el grafo")
    grafo = Grafo(ruta_mapa)
    
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# arcos   : {grafo.num_arcos}")

    # =========================================================================
    # PASO 2: Crear el algoritmo y ejecutar la busqueda
    # =========================================================================
    
    # Creamos el objeto algoritmo con el grafo y los nodos origen/destino
    algoritmo = Algoritmo(grafo, origen, destino)

    # Ejecutamos A* (que usa heuristica para ser mas rapido que Dijkstra)
    # Devuelve: el camino, el coste total, cuantos nodos expandio, y el tiempo
    print(f"\nBuscando camino de {origen} a {destino}...")
    
    resultado = algoritmo.a_estrella()  # Cambiar a .a_estrella() para usar A*
    camino = resultado[0]
    coste = resultado[1]
    num_expansiones = resultado[2]
    tiempo = resultado[3]

    # =========================================================================
    # PASO 3: Mostrar resultados y guardar en fichero
    # =========================================================================
    
    # Comprobamos si encontro camino
    if camino is None:
        print("No se ha encontrado ningun camino :(")
        print("Puede que los nodos no esten conectados o no existan.")
        sys.exit(1)

    # Mostramos los resultados por pantalla
    print(f"Solucion optima encontrada con coste {coste}")
    print(f"Tiempo de ejecucion: {tiempo:.2f} segundos")
    
    # Calculamos nodos por segundo (con cuidado de no dividir por 0)
    if tiempo > 0:
        nodos_por_segundo = num_expansiones / tiempo
        print(f"# expansiones: {num_expansiones} ({nodos_por_segundo:.2f} nodos/seg)")
    else:
        print(f"# expansiones: {num_expansiones} (tiempo muy pequeno)")

    # Guardamos el camino en el fichero de salida
    escribir_camino(grafo, camino, fichero_salida)
    print(f"\nCamino guardado en: {fichero_salida}")


# Esto hace que main() se ejecute cuando lanzamos el script directamente
# (pero no cuando lo importamos desde otro fichero)
if __name__ == "__main__":
    main()

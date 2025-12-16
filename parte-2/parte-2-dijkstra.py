#!/usr/bin/env python3
import sys
import os

from grafo import Grafo
from algoritmo import Algoritmo


def normalizar_ruta(nombre):
    """
    Si NO tiene ruta, asumimos que está en el mismo directorio que este script.
    Si tiene ruta (relativa o absoluta), lo dejamos tal cual.
    """
    if os.path.dirname(nombre):
        return nombre
    base = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base, nombre)


def escribir_camino(grafo, camino, fichero_salida):
    """
    Escribe el camino en el fichero con el formato:
    1 - (coste) - 308 - (coste) - 309
    """
    if not camino:
        return

    with open(fichero_salida, "w") as f:
        f.write(str(camino[0]))

        for u, v in zip(camino, camino[1:]):
            coste_uv = None
            for vecino, c in grafo.vecinos(u):
                if vecino == v:
                    coste_uv = c
                    break

            if coste_uv is None:
                raise ValueError(f"No se encontró arco {u}->{v} al escribir la solución.")

            f.write(f" - ({coste_uv}) - {v}")

        f.write("\n")


def main():
    if len(sys.argv) != 5:
        print("Uso: parte-2-dijkstra.py vertice-1 vertice-2 nombre-del-mapa fichero-salida")
        sys.exit(1)

    origen = int(sys.argv[1])
    destino = int(sys.argv[2])
    nombre_mapa = sys.argv[3]
    fichero_salida = sys.argv[4]

    ruta_mapa = normalizar_ruta(nombre_mapa)
    fichero_salida = normalizar_ruta(fichero_salida)

    grafo = Grafo(ruta_mapa)
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# arcos : {grafo.num_arcos}")

    alg = Algoritmo(grafo, origen, destino)

    # Ejecutamos DIJKSTRA (fuerza bruta, h=0, usando Dial)
    camino, coste, expansiones, tiempo = alg.dijkstra()

    if camino is None:
        print("No se ha encontrado ningún camino :(")
        sys.exit(1)

    print(f"Solución óptima encontrada con coste {coste}")
    print(f"Tiempo de ejecución: {tiempo:.2f} segundos")
    if tiempo > 0:
        print(f"# expansiones : {expansiones} ({expansiones/tiempo:.2f} nodes/sec)")
    else:
        print(f"# expansiones : {expansiones} (tiempo ≈ 0)")

    escribir_camino(grafo, camino, fichero_salida)


if __name__ == "__main__":
    main()

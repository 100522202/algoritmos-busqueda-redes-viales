import sys
import lector_entrada
import imprimir_solucion
import escribir_salida
import solver

#Todo: quitar ñ

def main():
    """Main de ejecucion principal"""

    if len(sys.argv) != 3:
        print("El formato correcto es parte-1.py <fichero_entrada> <fichero_salida>")
        sys.exit(1)

    fichero_entrada = sys.argv[1]
    fichero_salida = sys.argv[2]
    n, lista_fijas, lineas = lector_entrada.main(fichero_entrada)

    # Creamos una nueva instancia del problema para esta ejecucion
    problem = solver.crear_problema()

    # Creamos variables y añadimos las que ya tenemos
    solver.añadir_casilla_fija(problem, lista_fijas)
    solver.crear_variables(problem, n)

    # Agregamos restricciones
    solver.añadir_num_igual_de_fichas(problem, n)
    solver.añadir_restricciones_de_consecucion(problem, n)

    solution, num_solution = solver.obtener_solucion(problem)

    print(imprimir_solucion.imprimir_entrada_formato(lineas))
    print(f"{num_solution} soluciones encontradas")

    if solution is None:
        print("No hay solucion Problema insatisfacible")
        return

    escribir_salida.escribir_salida_fichero(fichero_salida, lineas, solution, n)


if __name__ == "__main__":
    main()

import sys
from constraint import ExactSumConstraint
import lector_entrada
import imprimir_solucion
import escribir_salida
import solver

def main():
    """Main de ejecución principal"""

    if len(sys.argv) !=3:
        print("El formato correcto es parte-1.py <fichero_entrada> <fichero_salida>")
        sys.exit(1)
    fichero_entrada = sys.argv[1]
    fichero_salida = sys.argv[2]
    n, lista_fijas, lineas = lector_entrada.main(fichero_entrada)
    #Creamos variables y añadimos las que ya tenemos

    solver.añadir_casilla_fija(lista_fijas)
    solver.crear_variables(n)

    #Agregamos restricciones
    solver.añadir_num_igual_de_fichas(n)

    solver.añadir_restricciones_de_consecucion(n)

    solution, num_solution = solver.obtener_solucion()

    if solution is None:
        return print("No hay solución Problema insatisfacible")
        

    escribir_salida.escribir_salida_fichero(fichero_salida, lineas, solution, n)

    print(imprimir_solucion.imprimir_entrada_formato(lineas))
    print(f"{num_solution} soluciones encontradas")

if __name__ == "__main__":
    main()
    


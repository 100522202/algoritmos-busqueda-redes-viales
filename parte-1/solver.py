import constraint
from constraint import ExactSumConstraint


def crear_problema():
    """Crea y devuelve una nueva instancia del problema CSP."""
    return constraint.Problem()


def añadir_casilla_fija(problem, lista_fijas):
    """MǸtodo que va a agregar una casilla fija por el fichero de entrada"""
    for casilla, valor in lista_fijas:
        problem.addVariable(casilla, [valor])


def crear_variables(problem, n):
    """Funcion que va a crear y agrear las variables al problema en base a un dominio
    y las dimensiones del tablero (n)"""

    #El dominio va a tomar 0 (negro) y 1 (blanco) para poder facilitar la definicion de restricciones
    dominio = [0, 1] 
    #vamos a definir a cada casilla como variable
    for i in range(n):
        for j in range(n):
            casilla = f"C{i}{j}"
            if casilla not in problem._variables:
                problem.addVariable(casilla, dominio)


def no_3_seguidos(i, j, k):
    """Restriccion que va a restringir mas de dos posiciones consecutivas con el mismo 
    color"""
    return not (i == j == k)

def añadir_num_igual_de_fichas(problem, n:int):
    """MǸtodo que va a añadir las restricciones para que se cumpla que haya 
    el mismo nǧmero de color de fichas tanto negras como blancas en la misma fila
    y en columnas"""
    
    for fila in range(n):
        fila_variables = []
        for col in range(n):
            fila_variables.append(f"C{fila}{col}")
        problem.addConstraint(ExactSumConstraint(n // 2), fila_variables)
    
    
    for col in range(n):
        columna_variables = []
        for fila in range(n):
            columna_variables.append(f"C{fila}{col}")
        problem.addConstraint(ExactSumConstraint(n // 2), columna_variables)


    
    

def añadir_restricciones_de_consecucion(problem, n):
    #Todo aañadir docstring
    #vamos a añadir las restricciones para las filas

    for fila in range(n):
        for col in range(n - 2):
            ci = f"C{fila}{col}"
            cj = f"C{fila}{col + 1}"
            ck = f"C{fila}{col + 2}"
            problem.addConstraint(no_3_seguidos, (ci, cj, ck))

    #Vamos a agregar la misma restriccion para las columnas
    for fila in range(n - 2):
        for col in range(n):
            ci = f"C{fila}{col}"
            cj = f"C{fila + 1}{col}"
            ck = f"C{fila + 2}{col}"
            problem.addConstraint(no_3_seguidos, (ci, cj, ck))

#Obtenemos las soluciones
def obtener_solucion(problem):
    solutions = problem.getSolutions()
    if not solutions:
        return  None, 0 
    return solutions[0], len(solutions)

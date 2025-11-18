def imprimir_solucion_formato(entrada:dict, n):
    """Método que va a imprimir en el formato que pide
    el enunciado """
    texto = ""

    #Linea superior
    texto = "+---" * n + "+\n"

    for fila in range(n):
        texto += "| "
        for col in range(n):
            valor = entrada[f"C{fila}{col}"]
            if valor == 1:
                texto += "O "
            else:
                texto += "X "
            texto += "| "
        texto += "\n"
    texto += "+---" * n + "+\n"

    return texto

def imprimir_entrada_formato(lineas):
    """Imprime el fichero de entrada en formato tablero"""

    n = len(lineas)

    texto = "+---" * n + "+\n"

    for fila in range(n):
        texto += "| "
        for col in range(n):
            c = lineas[fila][col]
            if c == '.':
                texto += "  | "
            elif c == 'X':
                texto += "X | "
            elif c == 'O':
                texto += "O | "
            else:
                raise ValueError(f"Carácter inválido: {c}")
        texto += "\n"
            
    texto += "+---" * n + "+\n"

    return texto




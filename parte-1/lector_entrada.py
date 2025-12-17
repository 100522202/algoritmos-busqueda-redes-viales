
def leer_fichero(fichero_entrada):

    lineas = []
    with open(fichero_entrada) as f: 
        for linea in f:
            linea_limpia = linea.strip()
            if linea_limpia != "": #si la linea no está vacia
                lineas.append(linea_limpia)

    #Número de filas columnas
    n = len(lineas)

    #Validamos que sea cuadrado
    for linea in lineas:
        if len(linea) != n:
            raise ValueError("El tablero dado no es cuadrado")
    
    return n, lineas


def procesar_casillas(n, lineas:list):
    """Método que va a procesar cada casilla"""
    lista_fijas = []
    for i in range(n):
        for j in range(n):
            caracter = lineas[i][j]

            casilla = f"C{i}_{j}"

            if caracter == 'X':
                lista_fijas.append((casilla, 0))
            elif caracter == 'O':
                lista_fijas.append((casilla, 1))
            elif caracter == '.':
                continue
            else:
                raise ValueError(f"Carácter inválido '{caracter}' en ({i},{j})")

    return lista_fijas

def main(ruta_fichero):
    n, lineas = leer_fichero(ruta_fichero)
    lista_fijas = procesar_casillas(n, lineas)
    return n, lista_fijas, lineas
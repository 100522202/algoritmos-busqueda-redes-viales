import imprimir_solucion

def escribir_salida_fichero(fichero_salida, lineas, solucion, n):
    """Función que va a escribir la solución en el archivo de salida dado por el enunciado"""
    
    texto_instancia = imprimir_solucion.imprimir_entrada_formato(lineas)
    texto_solucion = imprimir_solucion.imprimir_solucion_formato(solucion, n)
    
    with open(fichero_salida, "w", encoding="utf-8") as f:
        f.write(texto_instancia)
        f.write(texto_solucion)

        
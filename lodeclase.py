import constraint

p = constraint.Problem()

#el primero paso es resol edr la modelizacion de nuestro problema apapel y movil

p.addVariable("v1", ['rojo', 'verde', 'azul']) #variable nombre y su dominio

p.addVariables(["v2", "v3", "v4"], ['rojo', 'verde', 'azul'])

#Vamos a agregar restricciones
#p.addConstraint(RESTRICCION, iterable)

def distintoColor(vi, vj):
    """Devovlemos cierto si y solo si los vertices vi y vj se colorean diferentemente"""
    #Pero lo que recive en vi y vj no son las variablels, cuando llamar la fucnion llamara con todos 
    #los posilbes valroes de vi y vj
    return vi != vj


p.addConstraint(distintoColor, ["v1", "v2"]) #tenemos que pasar un tierable con dos variables, forzará que v1 y v2 tomen distinto color

p.addConstraint(distintoColor, ["v2", "v4"]) 

p.addConstraint(distintoColor, ["v3", "v4"]) 

p.addConstraint(distintoColor, ["v1", "v3"]) 

for isolution in p.getSolutions():
    print(isolution) #Devuelve un alista de diccionarios, la clave sera el nombre de las variables

#ponemos que v2 y v3 sean adyacentes
p.addConstraint(distintoColor, ["v2", "v3"])
p.addConstraint(distintoColor, ["v1", "v4"])

for isolution in p.getSolutions():
    print(isolution)
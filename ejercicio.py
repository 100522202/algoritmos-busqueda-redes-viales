#ejerciciod e send more money
import constraint
p = constraint.Problem()

p.addVariables("SENDMORY", range(10)) #POrque va del 0 hasta el 9
p.addVariables("abcd", range(2)) #Range 2 porque va del 0 al 1


def sumaLetras(u:int, v:int, r:int, post:int, pre:int = 0):
    #voy a necesitar 5 variabels el acarreo anterior la sa de las dos letras la resultante y el acarreo resultante
    return u + v + pre == r + 10*post

p.addConstraint(sumaLetras, "DEYd")

p.addConstraint(sumaLetras, "NREcd")

p.addConstraint(sumaLetras, "EONbc")

p.addConstraint(sumaLetras, "SMOab")

p.addConstraint(lambda x, y: x==y, "Ma")

p.addConstraint(constraint.AllDifferentConstraint (), "SENDMORY")

for isolution in p.getSolutions():
    print(isolution)
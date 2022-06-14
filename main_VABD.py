from math import *
from STANDARD_INPUT import *
from importlib import reload
import funcion_especial as fe

def leerArchivo(nombre):
    with open(nombre, 'r', encoding='utf-8-sig') as file:
        row0 = file.readline().split(';')
        row00 = row0[0]
        if row00 == 'Y\X':
            reverse = False
        elif row00 == 'X\Y':
            reverse = True
        else:
            print("Hubo un error en la lectura del archivo")
            return None, None, None, None

        xVals = row0[1:]
        xVals[-1].rstrip('\r\n')
        xVals = [int(x) for x in xVals]
        matProbConj = []
        yVals = []
        for linea in file:
            cruda = linea.split(';')
            if '' in cruda:
                break
            yVals.append(int(cruda[0]))
            cruda[-1].strip('\r\n')
            matProbConj.append([float(p) for p in cruda[1:]])

    # el siguiente if intercambia X e Y cuando la matriz esta dada en la forma 'X\Y'
    # luego de la siguiente transformacion, el resto del programa operara con un matriz de la forma 'Y\X'
    if reverse:
        aux = xVals
        xVals = yVals
        yVals = aux
        matProbConj = traspuesta(matProbConj)

    return xVals, yVals, matProbConj, reverse


def mostrarMatriz(mat):
    for fila in mat:
        for elemento in fila:
            print(round(elemento, 3), end='  \t')
        print()


def mostrarMatProbConj(pxy, rx, ry, reverse):
    if reverse:
        a00 = r"X\Y"
        rcol = ry
        rfil = rx
        datos = traspuesta(pxy)   # Revertimos el corregimiento que se hizo de la matriz en leerArchivo()
    else:
        a00 = r"Y\X"
        rfil = ry
        rcol = rx
        datos = pxy
    print(a00, end='\t')
    for c in rcol:
        print(c, end='\t')
    print()
    for i in range(len(datos)):
        print(rfil[i], end='  \t')
        for j in range(len(datos[0])):
            print(round(datos[i][j], 3), end='  \t')
        print()


def traspuesta(mat):
    filas = len(mat)
    columnas = len(mat[0])
    tras = [[] for k in range(columnas)]
    for i in range(columnas):
        tras[i] = [None for k in range(filas)]
    for i in range(columnas):
        for j in range(filas):
            tras[i][j] = mat[j][i]
    return tras


def indice(lista, elemento):
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    return None


def pMargY(mat):
    filas = len(mat)
    cols = len(mat[0])
    py = [0 for k in range(filas)]
    for i in range(filas):
        acum = 0
        for j in range(cols):
            acum += mat[i][j]*10     # multiplico y divido por 10 para solucionar problemas con el manejo de floats
        py[i] += acum/10
    return py


def pMargX(mat):
    return pMargY(traspuesta(mat))


def matValProb(rango, prob):   # devuelve una matriz que tiene como primera columna k y como segunda columna P(K=k)
    mat = []
    for i in range(len(rango)):
        mat.append([rango[i], prob[i]])
    return mat


def matXYcond(pxy, pcond, var):
    if var not in ['x', 'X', 'y', 'Y']:
        print("Error: var debe ser o X o Y")
        return None
    mat = []
    for i in range(len(pxy)):
        fila = []
        for j in range(len(pxy[0])):
            if var == 'x' or var == 'X':
                prob = pxy[i][j] / pcond[j]
            else:
                prob = pxy[i][j] / pcond[i]
            fila.append(prob)
        mat.append(fila)
    return mat


def E(X):  # X representa a la matriz que incluye al rango de X y a sus probabilidades asociadas
    acum = 0
    for i in range(len(X)):
        acum += X[i][0] * (X[i][1]*10)
    return round(acum/10, 3)


def V(X):  # X representa a la matriz que incluye al rango de X y a sus probabilidades asociadas
    X2 = []  # representa la VAD X**2
    for i in range(len(X)):
        X2.append([X[i][0]**2, X[i][1]])
    return round(E(X2) - E(X) ** 2, 3)


def XopY(matpxy, matpx, matpy, operacion):  # devuelve una lista de valores con sus probabilidades asociadas
    lista_resultados = []
    pXopY = []
    for i in range(len(matpxy)):
        for j in range(len(matpxy[0])):
            resultado = operacion(matpx[j][0], matpy[i][0])
            if resultado not in lista_resultados:
                if matpxy[i][j] != 0:
                    lista_resultados.append(resultado)
                    pXopY.append([resultado, matpxy[i][j]])
            else:
                pos = indice(lista_resultados, resultado)
                pXopY[pos][1] += matpxy[i][j]
    return pXopY


def XprodY(matpxy, matpx, matpy):
    return XopY(matpxy, matpx, matpy, lambda u, v: u*v)


def XmasY(matpxy, matpx, matpy):
    return XopY(matpxy, matpx, matpy, lambda u, v: u + v)


def cov(matpxy, matpx, matpy):
    return round(E(XprodY(matpxy, matpx, matpy)) - E(matpx) * E(matpy), 3)


def coefCorr(matpxy, matpx, matpy):
    return round(cov(matpxy, matpx, matpy) / (sqrt(V(matpx)) * sqrt(V(matpy))), 3)


def sonInd(mat):
    px = pMargX(mat)
    py = pMargY(mat)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if round(mat[i][j], 3) != round(px[j] * py[i], 3):
                return False
    return True


def probCond(mat, rx, ry, cond, cond2=None):
    if cond2 is not None:
        return probDado(mat, rx, ry, cond, cond2)
    acum = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if cond(rx[j], ry[i]):
                acum += mat[i][j]
    return round(acum, 3)


def probDado(mat, rx, ry, cond1, cond2):
    numerador = probCond(mat, rx, ry, lambda x, y : cond1(x,y) and cond2(x,y), None)
    denominador = probCond(mat, rx, ry, cond2, None)
    if denominador == 0:
        return 0
    return round(numerador/denominador, 3)


def escribirCondiciones():
    str_cond = input("Ingrese la condicion para X e Y en formato Python, usando '|' P(A|B): ")
    str_cond = str_cond.replace('|', ',')
    lineas = ['def cond_input(X, Y):\n', f"    return {str_cond}"]
    arch_funcion_esp = open("funcion_especial.py", "w")
    arch_funcion_esp.writelines(lineas)
    arch_funcion_esp.close()
    return str_cond.replace(',', '|')


def leerCondiciones():
    reload(fe)
    if type(fe.cond_input(0, 0)) is tuple:
        cond = lambda a, b: fe.cond_input(a, b)[0]
        cond2 = lambda a, b: fe.cond_input(a, b)[1]
    else:
        cond = fe.cond_input
        cond2 = None
    return cond, cond2


def main():
    rx, ry, pxy, reverse = leerArchivo('PROB_CONJ.csv')
    if reverse is None:
        return

    px = pMargX(pxy)
    py = pMargY(pxy)

    matpx = matValProb(rx, px)
    matpy = matValProb(ry, py)

    op = 1
    print('-' * 30 + "ANALISIS DE VAD BIDIMENSIONAL" + '-' * 30)
    print("\nMatriz de probabilidad conjunta: ")
    mostrarMatProbConj(pxy, rx, ry, reverse)
    print("\nMENU:"
          "\n1. Probabilidades maginales, valores esperados y varianzas"
          "\n2. Probabilidades condicionadas"
          "\n3. Probabilidades de la suma X+Y"
          "\n4. Probabilidades del producto XY"
          "\n5. Covarianza, correlacion e independencia"
          "\n6. Condicion especial para un suceso general")
    while op != 0:
        op = inputIntRango("\nElija una opcion. Para salir, ingrese 0: ", 0, 6)
        if op == 1:
            print("\nProbabilidades marginales de X:\nx  \tP(X=x) ")
            mostrarMatriz(matpx)
            print("\nProbabilidades marginales de Y:\ny  \tP(Y=y)")
            mostrarMatriz(matpy)

            print("\nE(X)=", E(matpx))
            print("E(Y)=", E(matpy))

            print("\nV(X)=", V(matpx))
            print("V(Y)=", V(matpy))
        elif op == 2:
            print("\nMatriz de probabilidades conjuntas condicionadas a X=x")
            matCondX = matXYcond(pxy, px, 'X')
            mostrarMatProbConj(matCondX, rx, ry, reverse)
            print("\nMatriz de probabilidades conjuntas condicionadas a Y=y")
            matCondY = matXYcond(pxy, py, 'Y')
            mostrarMatProbConj(matCondY, rx, ry, reverse)
        elif op == 3:
            suma = XmasY(pxy, matpx, matpy)
            print("\nDistribucion de probabilidades de la suma:\nk\tP(X+Y)=k")
            mostrarMatriz(suma)
            print("\nE(X+Y)=", E(suma))
            print("V(X+Y)=", V(suma))
        elif op == 4:
            prod = XprodY(pxy, matpx, matpy)
            print("\nDistribucion de probabilidades del producto:\nk\tP(XY)=k")
            mostrarMatriz(prod)
            print("\nE(XY)=", E(prod))
            print("V(XY)=", V(prod))
        elif op == 5:
            print("\ncov(X,Y)=", cov(pxy, matpx, matpy))
            print("coefcorr(X,Y)=", coefCorr(pxy, matpx, matpy))

            if sonInd(pxy):
                print("x e Y son independientes")
            else:
                print("X e Y NO son independientes")
        elif op == 6:
           str_cond = escribirCondiciones()
           cond, cond2 = leerCondiciones()
           print(f"\nP({str_cond}) =", probCond(pxy, rx, ry, cond, cond2))


main()


from math import sqrt
from numpy import mean
from scipy import stats as st
from STANDARD_INPUT import *
negar = ["no", "n", 'NO', 'No', 'no.', 'NO.', 'N']


def valoresObservados(n):
    x = []
    for i in range(n):
        i = inputFloat("Ingrese el " + str(i + 1) + "-esimo valor de x: ")
        x.append(i)
    xbar = mean(x)
    s = st.tstd(x)
    sn = st.sem(x)  # sn = s / sqrt(n)
    return xbar, s, sn


def inputParametrosMuestrales(n, dist):
    s, sn = None, None
    conoceXRaya = input("¿Conoce el valor de xRaya?: ")
    if conoceXRaya not in negar:
        xraya = inputFloat("Ingrese xRaya: ")
        if dist == 2:   # t-STUDENT: necesito tambien la s y la sn
            s = inputFloat("Ingrese el desvio estandar muestral: ")
            sn = s/sqrt(n)
    else:
        conoceDatos = input("¿Conoce los datos?: ")
        if conoceDatos not in negar:
            xraya, s, sn = valoresObservados(n)  # De aqui solo me importa el valor de xraya
        else:
            xraya = None
    if dist == 2:
        return xraya, s, sn
    return xraya


def valorZCrit(gamma, lat):
    if lat == 1:
        zCrit = st.norm.ppf(gamma)
    else:  # lat == 2:
        zCrit = st.norm.ppf((1+gamma)/2)

    return zCrit


def valorTCrit(gamma, n, lat):
    if lat == 1:
        tCrit = st.t.ppf(gamma, n-1)
    else: # lat == 2
        tCrit = st.t.ppf((1+gamma)/2, n-1)

    return tCrit


def valorNNorm(zCrit, sigma, error):
    while error < 0:
        error = inputFloat("Por favor, ingrese un numero positivo: ")
    return int(((sigma*zCrit)/error)**2) + 1


def mostrarIntervalos(xraya, delta, lat, prop=False):
    print("\nError para la media: ", round(delta, 3))
    if xraya is None:
        return

    if lat == 1:
        if prop:
            inf, sup = 0, 1
        else:
            inf, sup = '-inf,', '+inf'
        print("\nIntervalo de confianza superior de la media: ")
        print([inf, round(xraya + delta, 3)])
        print("\nIntervalo de confianza inferior de la media: ")
        print([round(xraya - delta, 3), sup])

    else:  # lat == 2
        print("\nIntervalo de confianza de la media: ")
        print([round(xraya - delta, 3), round(xraya + delta, 3)])


def main():
    print("----------INTERVALOS DE CONFIANZA----------")
    gamma = inputFloatRango("Ingrese el valor de gamma: ", 0, 1)
    lat = inputIntRango("¿Qué tipo de intervalo se pide?\n1. Unilateral\n2. Bilateral\n",1,2)
    print("¿Qué distribución sigue la media muestral?\n1. Z (Normal) \n2. T (t-Student)\n3. Proporcion (xRaya=pPico)")
    dist = inputIntRango("", 1, 3)

    # DIST. NORMAL
    if dist == 1:
        sigma = inputFloat("Ingrese sigma: ")
        zCrit = valorZCrit(gamma, lat)
        tamCon = input("¿Conoce el tamaño de la muestra?: ")
        if tamCon not in negar:
            n = inputNat("Ingrese el numero de elementos de la muestra: ")
        else:
            error = inputFloat("¿Cual es el error maximo que desea cometer?: ")
            n = valorNNorm(zCrit, sigma, error)
            print("\nSe debe tomar una muestra de", n, "elementos")

        xraya = inputParametrosMuestrales(n, dist)
        delta = zCrit*(sigma/sqrt(n))

        mostrarIntervalos(xraya, delta, lat)

    # DIST. t-STUDENT
    if dist == 2:
        n = inputNat("Ingrese el numero de elementos de la muestra: ")   # Se asume que es conocido
        xraya, s, sn = inputParametrosMuestrales(n, dist)
        tCrit = valorTCrit(gamma, n, lat)
        delta = tCrit*sn

        mostrarIntervalos(xraya, delta, lat)

    # PROPORCION
    if dist == 3:
        zCrit = valorZCrit(gamma, lat)
        conocePpico = input("¿Conoce el valor de pPico?: ")
        if conocePpico not in negar:
            pPico = inputFloatRango("Ingrese pPico: ", 0, 1)
            var = pPico * (1 - pPico)  # varianza de la variable aleatoria, sigma**2
        else:
            pPico = None
            var = 0.25
        tamCon = input("¿Conoce el tamaño de la muestra?: ")
        if tamCon not in negar:
            n = inputNat("Ingrese el numero de elementos de la muestra: ")
        else:
            error = inputFloat("¿Cual es el error maximo que desea cometer?: ")
            while error < 0:
                error = inputFloat("Por favor, ingrese un error positivo")
            nPeor = int((zCrit/(2*error))**2) + 1
            if pPico is None:
                n = nPeor
                print("\nSe debe tomar una muestra de tamaño", n)
            else:
                n = int(var*((zCrit/error)**2)) + 1
                print("\nEn el peor de los casos, bastaría con una muestra de", nPeor, "elemmentos")
                print("\nAsumiendo que p es aproximadamente el pPico indicado, basta con n =", n)

        delta = zCrit*sqrt(var/n)
        mostrarIntervalos(pPico, delta, lat, True)


main()
input()


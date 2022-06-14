from STANDARD_INPUT import *
from math import sqrt
import numpy as np
from scipy import stats as st
from matplotlib import pyplot as plt

negar = ["no", "n", 'NO', 'No', 'no.', 'NO.', 'N']


def valoresObservados(n):
    x = []
    for i in range(n):
        i = inputFloat("Ingrese el " + str(i + 1) + "-esimo valor de x: ")
        x.append(i)
    xbar = np.mean(x)
    s = st.tstd(x)
    sn = st.sem(x)  # sn = s / sqrt(n)
    return xbar, s, sn


def inputMediaMuestral(n):
    conoceXRaya = input("¿Conoce el valor de xRaya?: ")
    if conoceXRaya not in negar:
        xraya = inputFloat("Ingrese xRaya: ")
    else:
        conoceDatos = input("¿Conoce los datos?: ")
        if conoceDatos not in negar:
            xraya, s, sn = valoresObservados(n)  # De aqui solo me importa el valor de xraya
        else:
            xraya = None
    return xraya


def valorZCrit(Ha, alfa):
    if Ha == 1:  # Ha: mu < mu0
        zCrit = st.norm.ppf(alfa)
    elif Ha == 2:     # Ha: mu != mu0
        zCrit = st.norm.ppf(1-alfa/2)
    else:       # Ha: mu > mu0
        zCrit = st.norm.ppf(1-alfa)
    return zCrit


def valorTCrit(Ha, alfa, n):
    if Ha == 1:  # Ha: mu < mu0
        tCrit = st.t.ppf(alfa, n-1)
    elif Ha == 2:     # Ha: mu != mu0
        tCrit = -st.t.ppf(alfa/2, n-1)
    else:       # Ha: mu > mu0
        tCrit = st.t.ppf(1-alfa, n-1)
    return tCrit


def valorNNorm(Ha, alfa, mu0, betaMu1, mu1, sigma):
    zBeta = st.norm.ppf(betaMu1)

    # Ha: mu != mu0
    if Ha == 2:
        zAlfa2 = st.norm.ppf(alfa/2)
        n = int((sigma*(zAlfa2+zBeta) / (mu0 - mu1))**2) + 1

    # Ha: mu < mu0 || mu > mu0
    else:
        zAlfa = st.norm.ppf(alfa)
        n = int((sigma*(zAlfa+zBeta) / (mu0 - mu1))**2) + 1
    return n


def valorNProp(Ha, alfa, p0, p1, betap1):
    zBeta = st.norm.ppf(betap1)

    # prueba de dos colas
    if Ha == 2:
        zAlfa2 = st.norm.ppf(alfa/2)
        n = int(((zAlfa2*sqrt(p0*(1-p0)) + zBeta*sqrt(p1*(1-p1))) / (p1-p0))**2) + 1

    # prueba de una cola:
    else:
        zAlfa = st.norm.ppf(alfa)
        n = int(((zAlfa*sqrt(p0*(1-p0)) + zBeta*sqrt(p1*(1-p1))) / (p1-p0))**2) + 1
    return n


def criticosNormalesBilaterales(mu0, sigma, n, zCrit):
    xc1 = mu0 - (sigma / sqrt(n)) * zCrit
    xc2 = mu0 + (sigma / sqrt(n)) * zCrit
    return xc1, xc2


def criticoNormalUnilateral(mu0, sigma, n, zCrit):
    return mu0 + (sigma / sqrt(n)) * zCrit


def conclusionPruebaNormalBilateral(xraya, xc1, xc2, alfa, mu0, n, sigma):
    if xc1 <= xraya <= xc2:
        print("NO se rechaza H0 con nivel de significancia", alfa)
    else:
        print("Se rechaza H0")
    pValue = pValNorm(mu0, n, 2, sigma, xraya)
    print("p-value =", round(pValue, 3))


def conclusionPruebaNormalUnilateral(Ha, xraya, xc, alfa, mu0, n, sigma):
    if (Ha == 1 and xraya > xc) or (Ha == 3 and xraya < xc):
        print("NO se rechaza H0 con nivel de significancia", alfa)
    else:
        print("Se rechaza H0")
    pValue = pValNorm(mu0, n, Ha, sigma, xraya)
    print("p-value =", round(pValue, 3))


def pValNorm(mu0, n, Ha, sigma, xraya):
    if Ha == 1:   # Ha: mu < mu0
        pVal = st.norm.cdf((xraya - mu0) / (sigma / sqrt(n)))
    elif Ha == 2:     # Ha: mu != mu0
        pVal = 2 * (1 - st.norm.cdf(abs((xraya - mu0) / (sigma / sqrt(n)))))
    else:         # Ha: mu > mu0
        pVal = 1 - st.norm.cdf((xraya - mu0) / (sigma / sqrt(n)))
    return pVal


def pValT(Ha, tObs, n):
    if Ha == 1:   # Ha: mu < mu0
        pValue = st.t.cdf(tObs, n-1)
    elif Ha == 2:     # Ha: mu != mu0
        pValue = 2*st.t.cdf(-abs(tObs), n-1)
    else:         # Ha: mu > mu0
        pValue = 1 - st.t.cdf(tObs, n-1)
    return pValue


def conclusionAnalisisT(Ha, n, tObs, tCrit):
    if (Ha == 1 and tObs < tCrit) or (Ha == 2 and abs(tObs) > tCrit) or (Ha == 3 and tObs > tCrit):
        print("Se rechaza H0")
    else:
        print("No se rechaza H0")
    pValue = pValT(Ha, tObs, n)
    print("p-value =", round(pValue, 7))


def graficarBeta(mu, beta, prop=False):
    verGraf = input("¿Desea ver la grafica de la curva de operacion caracteristica?")
    if verGraf not in negar:
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        plt.plot(mu, beta(mu), color='red')
        plt.xlabel("$\\mu$")
        plt.ylabel("$\\beta$")
        if prop:
            media = 'p'
        else:
            media = 'mu'
        print(f"Se grafica la curva de operacion caracteristica de beta en funcion de {media}")
        plt.show()


def main():
    print("------PRUEBA DE HIPÓTESIS-------")
    mu0 = inputFloat("Ingrese mu0: ")
    alfa = inputFloatRango("Ingrese el nivel de significancia: ", 0, 1)
    Ha = inputIntRango("¿De qué tipo es la Ha?\n1. mu < mu0 (cola izquierda)\n2. mu != mu0 (dos colas)\n3. mu > mu0 (cola derecha)\n", 1, 3)
    dist = inputIntRango("¿Qué distribución sigue el estadístico de prueba?\n1. Z (Normal) \n2. T (t-Student)\n3. Proporcion (xRaya=pPico)\n", 1, 3)

    # DISTRIBUCION NORMAL
    if dist == 1:
        sigma = inputFloat("Ingrese sigma: ")
        zCrit = valorZCrit(Ha, alfa)
        tamCon = input("¿Conoce el tamaño de la muestra?: ")
        if tamCon not in negar:
            n = inputNat("Ingrese el numero de elementos de la muestra: ")
            nCal = False
            mu1 = None
            betaMu1 = None
        else:
            betaCon = input("¿Conoce algun valor de beta asociado a algún mu1?: ")
            if betaCon not in negar:
                mu1 = inputFloat("Ingrese el mu1: ")
                betaMu1 = inputFloatRango("Ingrese su beta asociado: ", 0, 1)
                n = valorNNorm(Ha, alfa, mu0, betaMu1, mu1, sigma)
                print("El tamaño de la muestra debe ser", n)
                nCal = True
            else:
                print("No hay suficiente informacion")
                return
        xraya = inputMediaMuestral(n)

        if Ha == 2:   # caso Ha: mu != mu0
            xc1, xc2 = criticosNormalesBilaterales(mu0, sigma, n, zCrit)
            print("Xc1 =", round(xc1, 3))
            print("Xc2 =", round(xc2, 3))

            # informo si rechaza o no, y calculo el pValue (solo es posible cuando se conoce xraya)
            if xraya is not None:
                conclusionPruebaNormalBilateral(xraya, xc1, xc2, alfa, mu0, n, sigma)

            beta = lambda mu : st.norm.cdf((xc2 - mu) / (sigma / sqrt(n))) - st.norm.cdf((xc1 - mu) / (sigma / sqrt(n)))
            mu = np.linspace(mu0 - sigma, mu0 + sigma, 100)

        else:    # caso Ha: prueba unilateral
            xc = criticoNormalUnilateral(mu0, sigma, n, zCrit)
            print("Xc =", round(xc, 3))

            # informo si rechaza o no, y calculo el pValue (solo es posible cuando se conoce xraya)
            if xraya is not None:
                conclusionPruebaNormalUnilateral(Ha, xraya, xc, alfa, mu0, n, sigma)

            # grafico Beta en funcion de mu
            if Ha == 1:   # Ha: mu < mu0
                beta = lambda mu : 1 - st.norm.cdf((xc - mu) / (sigma / sqrt(n)))
                mu = np.linspace(mu0 - sigma, mu0, 100)

            else:   # Ha: mu > mu0
                beta = lambda mu : st.norm.cdf((xc - mu) / (sigma / sqrt(n)))
                mu = np.linspace(mu0, mu0 + sigma, 100)
        graficarBeta(mu, beta)

        if nCal:
            print(f"Notese que b({mu1}) vale {round(beta(mu1), 3)}, <= {betaMu1}")

        mu1 = inputFloat("Indique algun valor de mu, y se informara su beta asociado: ")
        print(round(beta(mu1), 3))

    #  DISTRIBUCION T-STUDENT
    if dist == 2:
        n = inputNat("Ingrese el tamaño de la muestra: ")    # en los ejercicios de dist. T, siempre se sabe n
        tCrit = valorTCrit(Ha, alfa, n)
        conoceXRaya = input("¿Conoce el valor de xRaya y S?: ")
        if conoceXRaya not in negar:   # no uso la funcion antes definida para hallar xraya porque tambien quiero s
             xraya = inputFloat("Ingrese xRaya: ")
             s = inputFloat("Ingrese s: ")
             sn = s / sqrt(n)
        else:
            conoceDatos = input("¿Conoce los datos?: ")
            if conoceDatos not in negar:
                xraya, s, sn = valoresObservados(n)
                print("Xraya =", round(float(xraya), 3))
                print("s =", round(s, 3))
            else:
                print("No hay suficientes datos")
                return 0

        print("tCrit =", round(tCrit, 3))
        tObs = (xraya-mu0)/sn
        print("tObs =", round(tObs, 3))

        conclusionAnalisisT(Ha, n, tObs, tCrit)  # siempre se obtiene una conclusion

    #  PROPORCIONES
    if dist == 3:
        p0 = mu0
        sigma0 = sqrt(p0*(1-p0))
        zCrit = valorZCrit(Ha, alfa)
        tamCon = input("¿Conoce el tamaño de la muestra?: ")
        if tamCon not in negar:
            n = inputNat("Ingrese el numero de elementos de la muestra: ")
        else:
            betaCon = input("¿Conoce algun valor de beta asociado a algún p1?: ")
            if betaCon not in negar:
                p1 = inputFloatRango("Ingrese el p1: ", 0, 1)
                betap1 = inputFloatRango("Ingrese su beta asociado: ", 0, 1)
                n = valorNProp(Ha, alfa, p0, p1, betap1)
                print("El tamaño de la muestra debe ser", n)
            else:
                print("No hay suficiente informacion")
                return
            
        pPico = inputMediaMuestral(n)

        if Ha == 2:  # caso Ha: p != p0
            pc1, pc2 = criticosNormalesBilaterales(p0, sigma0, n, zCrit)
            print("pc1 =", round(pc1, 3))
            print("pc2 =", round(pc2, 3))

            if pPico is not None:
                conclusionPruebaNormalBilateral(pPico, pc1, pc2, alfa, p0, n, sigma0)

            beta = lambda p : st.norm.cdf((pc2 - p) / (sqrt(p*(1-p)) / sqrt(n))) - st.norm.cdf((pc1 - p) / (sqrt(p*(1-p)) / sqrt(n)))
            p = np.linspace(p0 - sigma0, p0 + sigma0, 100)

        else:      # caso Ha: prueba unilateral
            pc = criticoNormalUnilateral(p0, sigma0, n, zCrit)
            print("pc =", round(pc, 3))

            # informo si rechaza o no, y calculo el pValue (solo es posible cuando se conocepPico pPico)
            if pPico is not None:
                conclusionPruebaNormalUnilateral(Ha, pPico, pc, alfa, p0, n, sigma0)

            # grafico Beta en funcion de p
            if Ha == 1:  # Ha: p < p0
                beta = lambda p : 1 - st.norm.cdf((pc - p) / (sqrt(p*(1-p)) / sqrt(n)))
                p = np.linspace(p0 - sigma0, p0, 100)

            else:  # Ha: p > p0
                beta = lambda p: st.norm.cdf((pc - p) / (sqrt(p*(1-p)) / sqrt(n)))
                p = np.linspace(p0, p0 + sigma0, 100)
        graficarBeta(p, np.vectorize(beta), True)
        p1 = inputFloat("Indique algun valor de p, y se informara su beta asociado: ")
        print(round(beta(p1), 3))


main()
input()

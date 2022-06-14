# FUNCIONES GENERALIZADAS

def inputTipo(mensaje, tipo):
    num = None
    done = False
    while not done:
        try:
            num = tipo(input(mensaje))
            done = True
        except ValueError:
            print("ERROR: respete el formato pedido\n")
    return num


def chequearInputCondicion(num, mensaje_error, tipo, cond):
    while not cond(num):
        num = inputTipo(mensaje_error, tipo)
    return num


def inputTipoCond(mensaje, tipo, cond):
    num = inputTipo(mensaje, tipo)
    return chequearInputCondicion(num, "Intente nuevamente:", tipo, cond)


def inputTipocota(mensaje, tipo, cota, sup):
    if sup:
        cond = lambda x: x < cota
        operador = 'menor'
    else:
        cond = lambda x: x > cota
        operador = 'mayor'
    mensaje_error = 'Por favor, ingrese un numero ' + operador + ' que ' + str(cota) + ': '
    return inputTipoCond(mensaje, tipo, cond)
    
    
def inputTipoRango(mensaje, inf, sup, tipo):
    cond = lambda x: inf <= x <= sup
    mensaje_error = "Por favor, ingrese un numero entre "+str(inf)+" y "+str(sup)+": "
    return inputTipoCond(mensaje, tipo, cond)


# FUNCIONES PARA INT

def inputInt(mensaje):
    return inputTipo(mensaje, int)


def inputIntCond(mensaje, cond):
    return inputTipoCond(mensaje, int, cond)


def inputIntDesde(mensaje, cota):
    return inputTipocota(mensaje, int, cota, False)


def inputIntHasta(mensaje, cota):
    return inputTipocota(mensaje, int, cota, True)


def inputIntRango(mensaje, inf, sup):
    return inputTipoRango(mensaje, inf, sup, int)


def inputNat(mensaje):
    return inputIntDesde(mensaje, 0)


# FUNCIONES PARA FLOAT

def inputFloat(mensaje):
    return inputTipo(mensaje, float)


def inputFloatCond(mensaje, cond):
    return inputTipoCond(mensaje, float, cond)


def inputFloatDesde(mensaje, cota):
    return inputTipocota(mensaje, float, cota, False)


def inputFloatHasta(mensaje, cota):
    return inputTipocota(mensaje, float, cota, True)


def inputFloatRango(mensaje, inf, sup):
    return inputTipoRango(mensaje, inf, sup, float)

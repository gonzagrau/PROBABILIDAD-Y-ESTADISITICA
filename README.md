# PROBABILIDAD-Y-ESTADISITICA
Programas didácticos para un curso introductorio a la probabilidad y estadística

---------------------------------------ESTIMACION DE PARAMETROS---------------------------------------

Este programa le permitirá estimar la media de una distribución poblacional a partir de la media
muestral Xraya. Estos intervalos pueden ser uni o bilaterales, y la media se puede estandarizar
con una distribución normal de sigma conocida, con la distribución t-Student, o con una propocion.

Se le pedirá que indique el nivel de confianza gamma, y el tipo de intervalo que desea. Luego, se 
le preguntará sobre la distribución que toma la media estandarizada.

INGRESO DEL TAMAÑO DE LA MUESTRA: Si lo conoce, ingreselo directamente. De no conocerlo,
se le pedirán datos adicionales que son necesarios para determinar cuanto debe valer n
para cumplir con el gamma ingresado y acotar el error con un valor maximo dado.

INGRESO DE LA MEDIA: Si conoce exactamente el valor de la media muestral, ingreselo. 
Si en particular la distribucion del estadistico de prueba es t-Student, también se le 
pedirá que ingrese la varianza muestral. De no saber cuando vale xRaya, si conoce los datos, 
se le pedira  que los ingrese uno a uno. De no conocer ni el valor de la media medida ni los 
datos, el programa procederá a mostrarle todo lo que se puede saber con un análisis pre-muestra.

El programa le mostrará por pantalla los intervalos de confianza, indicando el error cometido. En
particular, si el tamaño de n fue calculado, este también se informará por pantalla.


--------------------ANALISIS DE VARIABLE ALEATORIA BIDIMENSIONAL DISCRETA--------------------

Este programa permite analizar una parámetros de una variable aleatoria bidemensional
discreta a partir de su matriz de probabilidad conjunta.

Para ello, se debe guardar en un archivo llamado "PROB_CONJ.csv" dicha matriz, tal que:

1. La celda A1 indique el patron de lectura: Y\X o X\Y, segun corresponda
2. La primera fila y la primera columna (sin contar A1) contienen los rangos de X e Y
3. Las celdas LetraNumero de la tabla representan P(X=Letra1, Y=ANumero) o viceversa

Se adjunta en este .zip un ejemplo de archivo PROB_CONJ.csv, el cual se puede editar directamente

Se incluyen tambien los modulos STANDARD_INPUT.py y funcion_especial.py, los cuales se
deben guardar en la misma carpeta que main.py. Para correr el programa, ejecutar el main

Se le mostrará la matriz leida del .csv, y se desplegará un menú. Seguir las instrucciones.

IMPORTANTE: Para la opcion 6, ingrese las condiciones con formato Python. Por ejemplo:

X==Y
abs(X-Y) >= 2
min(X,Y) == 3

Para probabilidades condicionales A | B,  use el caracter '|' :

Y == 4 | Y>=2
Y == 2*X | X<5


---------------------------------------PRUEBA DE HIPOTESIS---------------------------------------

Este programa le permitirá hacer pruebas de hipótesis sobre la media muestra, para los
tres tipos de pruebas (cola izq., cola der., dos colas), para los tres tipos de distribuciones
del estadístico de prueba (normal con sigma conocida, t-Student, proporción).

Recuerde descargar en una misma carpeta main.py (el ejecutable) y STANDARD_INPUT.py (libreria)
A su vez, se requiere tener instalados los modulos numpy, scipy y matplotlib.

El programa le pedirá que ingrese el nivel de significancia, la hipotesis alternativa, y la 
distribucion del estadistico de prueba. 

INGRESO DEL TAMAÑO DE LA MUESTRA: Si lo conoce, ingreselo directamente. De no conocerlo,
se le pedirán datos adicionales que son necesarios para determinar cuanto debe valer n
para cumplir con el nivel de significancia ingresado y acotar el error de tipo 2 para algun 
valor dado de mu.

INGRESO DE LA MEDIA: Si conoce exactamente el valor de la media muestral, ingreselo. 
Si en particular la distribucion del estadistico de prueba es t-Student, también se le 
pedirá que ingrese la varianza muestral. De no saber cuando vale xRaya, si conoce los datos, 
se le pedira  que los ingrese uno a uno. De no conocer ni el valor de la media medida ni los 
datos, el programa procederá a mostrarle todo lo que se puede saber con un análisis pre-muestra.

Se visualizarán entonces los valores de corte, la gráfica de la curva de operación 
característica (para normal y proporción), y de conocerse la media muestral se aceptará
o se rechazará la hipótesis nula. Se le permitirá también ingresar un valor de mu para
calcular su error de tipo 2 asociado. De conocerse la media muestral, se informará también
el p-value.

OBSERVACIÓN: Si solo le interesa conocer el p-value, cuando se le pida ingresar el nivel de 
significancia simplemente ingrese un valor generico (como, por ejemplo, 0.05). Ignore los 
demás resultados.
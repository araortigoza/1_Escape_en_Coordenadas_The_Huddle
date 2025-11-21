import random
import heapq

CAMINO = 0
EDIFICIO = 1
AGUA = 2
ZONAS_BLOQ = 3


# CREA UN TABLERO LLENO DE CAMINOS LIBRES
def crear_tablero(filas, columnas):
    tablero = [[CAMINO for c in range(columnas)] for f in range(filas)]
    return tablero



# AGREGA EN MI TABLERO CAMINOS CADA 3 FILAS Y COLUMNAS
def crear_rutas_y_obs(filas, columnas, tablero):
    for f in range(filas):
        for c in range(columnas):
            if f % 3 == 0 or c % 3 == 0: # ESTO HACE QUE CADA 3 FILAS Y CADA 3 COLUMNAS HAYA UN CAMINO
                tablero[f][c] = CAMINO
            else:
                tablero[f][c] = EDIFICIO



# VALIDA QUE EL USUARIO NO SE POSICIONE FUERA DEL MAPA NI EN ALGUN OBSTACULO EXISTENTE
def validar_coordenadas(coordenada, filas, columnas, tablero):
        x, y = coordenada

        if 0 <= x < filas and 0 <= y < columnas:
            if tablero[x][y] == CAMINO:
                return True
        return False
        


# def imprimir_tablero(tablero):
#     print("\n")
#     for fila in tablero:
#         print("  ".join(str(celda) for celda in fila))
#     print("\n")



# AGREGA AL MAPA LOS EMOJIS CORRESPONDIENTES
def agregar_emojis(inicio, fin, camino, filas, columnas, tablero):
    for f in range(filas):
        fila_emojis = []
        for c in range(columnas):
            if (f, c) == inicio:
                fila_emojis.append("🚘")  # INICIO

            elif (f, c) == fin:
                fila_emojis.append("❎")  # FIN
            
            elif camino and (f, c) in camino:
                fila_emojis.append("🔸")  # CAMINO ENCONTRADO

            elif tablero[f][c] == EDIFICIO:
                fila_emojis.append("🏠")  # CASA

            elif tablero[f][c] == CAMINO:
                fila_emojis.append("⬜")  # CAMINO

            elif tablero[f][c] == AGUA:
                fila_emojis.append("💧")  # AGUA

            elif tablero[f][c] == ZONAS_BLOQ:
                fila_emojis.append("🚧")  # ZONA RESTRINGIDA
            

        print(" ".join(fila_emojis))



# AGREGA AGUA DE MANERA RANDOM AL MAPA EN UN 15%
def agregar_agua_random(tablero, filas, columnas):
    for f in range(filas):
        for c in range(columnas):
            if tablero[f][c] == CAMINO:
                if random.random() < 0.15:
                    tablero[f][c] = AGUA
    agregar_emojis(inicio, fin, None, filas, columnas, tablero)



# AGREGA LOS OBSTACULOS DEL USUARIO EN EL MAPA Y VALIDA QUE NO ESTE FUERA DEL MAPA NI ENCIMA DE OTROS OBSTACULOS
def agregar_zonas_bloq(tablero, filas, columnas):
    while True:
        obst_si_no = input("¿Desea agregar un obstáculo en el tablero? (si/no): ")
        if obst_si_no == "no":
            break
        
        elif obst_si_no == "si":
            fila_obst, columna_obst = map(int, input("Ingrese la fila y columna del obstaculo, separadas por coma (ej: 0,0): ").split(","))
            obst_usuario = (fila_obst, columna_obst)

            if validar_coordenadas(obst_usuario, filas, columnas, tablero):
                tablero[fila_obst][columna_obst] = ZONAS_BLOQ
                agregar_emojis(inicio, fin, None, filas, columnas, tablero)
                print("El obstaculo se agrego con exito")

            else:
                print("Coordenada invalida, vuelva a ingresar")
        
        else:
            print("Caracter invalido, ingrese si o no")



# AQUI EMPIEZA LO RELACIONADO AL ALGORITMO A-STAR
# DETERMINAMOS EL PESO/COSTO DE CADA CELDA DEL MAPA
PESOS = {
    CAMINO: 1,
    AGUA: 5,
    EDIFICIO: float("inf"),
    ZONAS_BLOQ: float("inf")
}


# CALCULA LA DISTANCIA ENTRE UN NODO HASTA LA POSICION FINAL - UTILIZA LA DISTANCIA MANHATTAN
def heuristica(nodo, fin):
    return abs(nodo[0] - fin[0]) + abs(nodo[1] - fin[1]) 


# COMIENZA EL ALGORITMO A-STAR
def A_Star(tablero, inicio, fin, pesos):
    # SE CREA LA COLA DE PRIORIDAD (OPEN_LIST)
    open_list = []
    heapq.heappush(open_list, (0, inicio))
    
    # SE CREAN DICCIONARIOS PARA IR REGISTRANDO EL COSTO Y EL PADRE DE CADA NODO
    g_score = {inicio: 0}
    padres = {inicio: None}
    
    # SE CREA UNA LISTA DE TUPLAS DE LAS DIRECCIONES (ARRIBA, ABAJO, IZQUIERDA, DERECHA)
    direcciones = [(0,1), (0,-1), (1,0), (-1,0)]
    

    while open_list:
        # SE EXTRAE DE LA COLA SOLO EL NODO DEL PRIMER ELEMENTO Y LO DEFINIMOS COMO NODO ACTUAL
        _, nodo_actual = heapq.heappop(open_list) 
        
        # SI LLEGAMOS AL FINAL, MARCAMOS EL CAMINO
        if nodo_actual == fin:
            return reconstruir_camino(padres, fin)
        
        # SE RECORRE LA LISTA DE DIRECCIONES
        for direccionx, direcciony in direcciones:
            # SE DEFINE QUE VECINO VAMOS A EXPLORAR
            vecino = (nodo_actual[0] + direccionx, nodo_actual[1] + direcciony) 
            fila, columna = vecino
            
            # VALIDA SI ESTAMOS DENTRO DEL MAPA
            if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
                # SI ES UN OBSTACULO NO TRANSITABLE, LO IGNORAMOS
                if tablero[fila][columna] == ZONAS_BLOQ or tablero[fila][columna] == EDIFICIO:
                    continue

                # SE CALCULA EL COSTO ACUMULADO DEL VECINO
                nuevo_g = g_score[nodo_actual] + pesos.get(tablero[fila][columna], 1)
                
                # VERIFICA QUE EL VECINO NO SE ENCUENTRE EN EL DICCIONARIO DE COSTOS O SI G ES MENOR AL YA EXISTENTE
                if vecino not in g_score or nuevo_g < g_score[vecino]:
                    padres[vecino] = nodo_actual # SE AGREGA COMO PADRE DEL VECINO EL NODO ACTUAL
                    g_score[vecino] = nuevo_g # SE AGREGA EL COSTO DEL VECINO
                    f_score = nuevo_g + heuristica(vecino, fin) # SE CALCULA F_SCORE (f = g + h)
                    heapq.heappush(open_list, (f_score, vecino)) # SE AGREGA A LA COLA DE PRIORIDAD F_SCORE Y EL NODO VECINO
    
    return None  # RETORNA NONE SI NO SE ENCONTRO CAMINO



# SE MARCA EL CAMINO RECORRIDO
def reconstruir_camino(padres, nodo):
    camino = [] # SE CREA UNA LISTA VACIA "CAMINO" PARA IR AGREGANDO LOS NODOS DESDE EL FINAL HASTA EL INICIO
    while nodo is not None:
        camino.append(nodo) # AGREGA EL NOTO ACTUAL AL FINAL DE LA LISTA
        nodo = padres[nodo] # AVANZAMOS AL PADRE DEL NODO ACTUAL
    return camino[::-1] # RETORNAMOS LA LISTA INVERTIDA (DESDE EL INICIO HASTA EL FINAL)


# LLAMAMOS A NUESTRAS FUNCIONES PARA AGREGAR ZONAS BLOQUEADAS Y AGUA RANDOM, LUEGO PROCEDEMOS A BUSCAR EL CAMINO CON A-STAR
def ejecutar_busqueda(tablero, inicio, fin, filas, columnas):
    agregar_zonas_bloq(tablero, filas, columnas)
    agregar_agua_random(tablero, filas, columnas)

    camino = A_Star(tablero, inicio, fin, PESOS)
    
    if camino:
        print("\nCamino encontrado:")
        agregar_emojis(inicio, fin, camino, filas, columnas, tablero)
    else:
        print("\nNo existe un camino válido 🚫")



# ---- PROGRAMA PRINCIPAL ----

filas = int(input("Ingrese la cantidad de filas: "))

columnas = int(input("Ingrese la cantidad de columnas: "))

tablero = crear_tablero(filas, columnas) 

crear_rutas_y_obs(filas, columnas, tablero)

agregar_emojis(None, None, None, filas, columnas,tablero)


# WHILE PARA PEDIR AL USUARIO COORDENADAS DE INICIO HASTA QUE SEAN VALIDAS
while True:
    # PIDE AL USUARIO EL INICIO EN UNA SOLA LINEA
    fila_inicio, columna_inicio = map(int, input("Ingrese la fila y columna de inicio, separadas por coma (ej: 0,0): ").split(","))
    inicio = (fila_inicio, columna_inicio)

    if validar_coordenadas(inicio, filas, columnas, tablero):
        break
    else:
        print("Coordenada invalida, vuelva a ingresar")

agregar_emojis(inicio, None, None, filas, columnas, tablero)


# WHILE PARA PEDIR AL USUARIO COORDENADAS DE FIN HASTA QUE SEAN VALIDAS
while True:
    # PIDE AL USUARIO EL FINAL EN UNA LINEA 
    fila_fin, columna_fin = map(int, input("Ingrese la fila y columna de fin, separadas por coma (ej: 5,7): ").split(","))
    fin = (fila_fin, columna_fin)

    if validar_coordenadas(fin, filas, columnas, tablero):
        break
    else:
        print("Coordenada invalida, vuelva a ingresar")

agregar_emojis(inicio, fin, None, filas, columnas, tablero)


# LLAMAMOS A ESTA FUNCION DOS VECES PARA QUE LUEGO DE ENCONTRAR EL CAMINO PUEDA REALIZAR EL RECALCULADO DE CAMINOS EN CASO DE QUERER AGREGAR OTRA ZONA BLOQUEADA

ejecutar_busqueda(tablero, inicio, fin, filas, columnas)

ejecutar_busqueda(tablero, inicio, fin, filas, columnas)










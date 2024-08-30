from tablero import *

##### Se añade una nueva clase al código para asociar un conjunto de variables a una sola casilla del tablero #####
class Variable:
    def __init__(self,fila,col,valor) -> None:
        self.fila = fila
        self.col = col
        self.valor = valor
        self.dominio = set()        # Un conjunto donde se van a almacenar los valores del dominio de cada variable

        self.podado = set()         # Un conjunto donde se van a almacenar las podas realizadas
        return

class Solver:
    def __init__(self) -> None:
        self.numBackJumps = 0
        self.calcularDominios = True    # Variable que indica si se calculan los dominios o ya se han calculado con otro método
        self.calcularVariables = True   # Variable que indica si se calculan las variables o ya se han calculado con otro método
        self.matriz_variables = [[None for _ in range(COLS)] for _ in range(FILAS)]  # Se inicializa la matriz de variables vacia
        return
    
    def notificarFicheroCargado(self):
        self.calcularDominios = True    # Al cargar un nuevo fichero, esta variable indica si se deben calcular (True) o no (False) los dominios
        self.calcularVariables = True   # Al cargar un nuevo fichero, esta variable indica si se deben calcular (True) o no (False) las variables de una casilla

        return

######################################################################################################################
#####                                                BACKTRACKING                                                #####
######################################################################################################################

    ##### Esta función se encarga de inicializar la matriz de variables #####
    def inicializar_matriz(self, tablero):

        if self.calcularVariables == True:                                              # Se comprueba que la matriz de variables no se haya inicializado antes en AC3
            for fila in range(FILAS):                                                   # Recorre la matriz
                for col in range(COLS):
                    valor = tablero.getCasilla(fila, col)                               # Coge el valor que hay en esa posición
                    if valor != 0:                                                      # Si es un número distinto de 0
                        self.matriz_variables[fila][col] = Variable(fila, col, valor)   # lo añade a la matriz de variables  
                    else:                                                               # Si es 0, 
                        self.matriz_variables[fila][col] = Variable(fila, col, None)    # la variable 'valor' la pone a 'None' (vacia)
                    
            self.calcularVariables = False                                              # Ponemos a false esta variable para que en caso de que se ejecute antes el AC3 no se vuelva a calcular
        return 


    ##### Calcula los posibles dominios para una casilla #####
    def calcular_dominios(self, tablero, fila, col):
        
        if self.matriz_variables[fila][col].valor is not None:  # Si la casilla ya tiene un valor
            return {self.matriz_variables[fila][col].valor}     # Su dominio será ese valor
        else:                                                   # Si la variable de valor está inicializada a 'None' (vacia), se calcula su dominio
            dominios = set(range(1,10))                         # Se inicializa un dominio del 1 al 9
            for valor in range(1,10):                           # Se comprueban las restricciones para cada número
                if tablero.estaEnFila(fila,col,valor) or \
                    tablero.estaEnCol(fila,col,valor) or \
                    tablero.estaEnMiniTablero(fila,col,valor):
                                                                
                    dominios.discard(valor)                     # Si el número infringe una restricción, se descarta del dominio                    
                                                                
        return dominios                                         # Se devuelve el dominio para cada posición
        
    ##### Se encarga de asociar cada vector de dominios calculado en la función anterior, a la variable 'dominio' de la matriz de variables #####
    def inicializar_dominios(self,tablero):
        if self.calcularDominios == True:                                                               # Se comprueba que los dominios no se hayan inicializado antes en AC3
            for fila in range(FILAS):                                                                   # Se recorre la matriz
                for col in range(COLS):
                    self.matriz_variables[fila][col].dominio = self.calcular_dominios(tablero,fila,col) # Se asocia cada dominio a su fila y columna correspondiente
    
            self.calcularDominios = False                                                               # Ponemos a false esta variable para que en caso de que se ejecute antes el AC3 no se vuelva a calcular


    ##### FUNCIÓN RECURSIVA DE BACKTRACKING #####
    def backtracking(self, tablero, fila, col):
        
        if tablero.esTableroCompleto():                             # CASO BASE: Si el tablero ya está lleno, devuelve true
            return True
        
        ## Ahora buscamos una casilla que esté vacía ##
        elif tablero.getCasilla(fila, col) != 0:                    # Si la casilla no es 0.. (está ocupada)
            if col < COLS - 1:                                      # Pasamos a la siguiente columna asegurandonos de que seguimos dentro de los límites del tablero
                return self.backtracking(tablero, fila, col + 1)
            elif fila < FILAS - 1:                                  # Pasamos a la siguiente fila asegurandonos de que seguimos dentro de los límites del tablero
                return self.backtracking(tablero, fila + 1, 0)
            else:
                return True                                        
        
        # Si la casilla está vacia..
        # Con el vector de dominios calculados para esa casilla, lo recorremos probando cada valor
        for valor in self.matriz_variables[fila][col].dominio:
            if not tablero.estaEnFila(fila,col,valor) and \
                not tablero.estaEnCol(fila,col,valor) and \
                not tablero.estaEnMiniTablero(fila,col,valor):      # Si el valor no infringe ninguna restricción

                tablero.setCasilla(fila, col, valor)                # Se coloca en la fila y columna correspondiente
                
                # Una vez colocado un valor del dominio, llamamos recursivamente a backtracking 
                if col < COLS - 1:
                    if self.backtracking(tablero, fila, col + 1):
                        return True
                elif fila < FILAS - 1:
                    if self.backtracking(tablero, fila + 1, 0):
                        return True
                else:
                    return True
                
                                                                    # Si no se puede colocar el valor, restablece la casilla a vacía para retroceder y probar con otro valor
                tablero.setCasilla(fila, col, 0)
                self.numBackJumps += 1                              # Sumamos 1 salto cada vez que se retroceda

    

    ##### Función encargada de ejecutar el Backtracking #####
    def ejecutarBackTracking(self, tablero):
        self.numBackJumps = 0

        self.inicializar_matriz(tablero)            # Inicializamos la matriz de variables
        self.inicializar_dominios(tablero)          # y los dominios al ejecutar el backtracking

        if self.backtracking(tablero, 0, 0):        # Llama a la función de backtracking con la posición inicial (0,0)
            text = "BackTracking: {} saltos atrás" 
            print(text.format(self.numBackJumps))
            return True
        else:
            return False

###################
# CONSIDERACIONES #
###################
#
# 1. Se utiliza 'None' en vez de 0 para no confundir entre un valor real '0' y una casilla vacía
#
# 2. Se utilizan conjuntos 'set()' en vez de listas '[]' porque estos no permiten duplicados y como un dominio
#    no pueden tener valores repetidos en su interior, se utilizan conjuntos.
#
# 3 En la función 'calcular_dominios' se utiliza 'discard' en vez de 'remove' para que no de error en caso de que el
#   elemento no esté en el dominio   

######################################################################################################################
#####                                                AC3                                                         #####
######################################################################################################################

    ##### Esta función devuelve el vector de aristas de celdas que tienen restriccion entre ellas ######
    def generar_restricciones(self):
        aristas = set()
        
        for fila in range(FILAS):                                   # Recorre la matriz
            for col in range(COLS):
                                        
                for i in range(FILAS):                              # Recorre la fila a la que pertenece la casilla actual
                    if i != col:                                    # Para no añadir la celda actual
                        aristas.add(((fila, col), (fila, i)))       # Se añade la casilla actual y la casilla con la que hay restricción (arista)
                
                for j in range(COLS):                               # Recorre la columna a la que pertenece la casilla actual
                    if j != fila:                                   # Para no añadir la celda actual
                        aristas.add(((fila, col), (j, col)))        # Se añade la casilla actual y la casilla con la que hay restricción (arista)
                
                stride = 3                                          # Recorre el mini tablero al que pertenece la casilla actual
                filaTablero = int(int(fila)/3) * stride             # Misma estructura que la función "estaEnMiniTablero"
                colTablero = int(int(col)/3) * stride
                for it_fila in range(stride):
                    for it_col in range(stride):
                        if filaTablero+it_fila != fila and colTablero+it_col != col:                # Para no añadir la celda actual
                            aristas.add(((fila, col), (filaTablero+it_fila, colTablero+it_col)))    # Se añade la casilla actual y la casilla con la que hay restricción (arista)
        
        return aristas      # Devuelve el conjunto de aristas final

    ##### Esta función se encarga de hacer cambios (o no) en los dominios de las casillas #####
    def reducir_dominios(self, i, j):
        cambios = False

        # i/j[0] y i/j[1] accede a la variable fila y col de la clase 'Variable'
        dominio_i = self.matriz_variables[i[0]][i[1]].dominio   # Obtiene el dominio de la casilla actual
        dominio_j = self.matriz_variables[j[0]][j[1]].dominio   # Obtiene el dominio de la casilla a la que se apunta

        for valor_i in dominio_i.copy():                        # Recorremos los valores del dominio de la casilla actual
            for valor_j in dominio_j:                           # Recorremos los valores del dominio de la casilla a la que se apunta
                if valor_i != valor_j:                          # Si no se repiten los valores en ambos dominios
                    break                                       # es consistente
            else:                                               # Si sí se repiten los valores en ambos dominos, es inconsistente
                dominio_i.remove(valor_i)                       # se elimina el valor del dominio de la casilla actual
                cambios = True                                  # se actualiza la variable booleana porque sí hemos hecho cambios en el dominio

        return cambios                                          # Se informa de si se han hecho cambios en el dominio o no

    # Esta función se encarga de almacenar los vecinos de una celda, es decir, las celdas que hay en la misma fila, columna y mini-tablero
    # Misma estructura que declarar_restricciones
    def obtener_vecinos(self, i):
        fila, col = i
        vecinos = set()

        for j in range(COLS):                       # Recorre la columna a la que pertenece la casilla actual
            if j != fila:                           # Para no añadir la celda actual
                vecinos.add((j, col))               # Se añade esa casilla al conjunto de 'vecinos'
        for k in range(FILAS):                      # Recorre la fila a la que pertenece la casilla actual
            if k != col:                            # Para no añadir la celda actual
                vecinos.add((fila, k))              # Se añade esa casilla al conjunto de 'vecinos'

        stride = 3                                  # Recorre el mini tablero al que pertenece la casilla actual
        filaTablero = int(int(fila)/3) * stride     # Misma estructura que la función "estaEnMiniTablero"
        colTablero = int(int(col)/3) * stride
        for it_fila in range(stride):
            for it_col in range(stride):
                if filaTablero+it_fila != fila and colTablero+it_col != col:    # Para no añadir la celda actual
                    vecinos.add((filaTablero+it_fila, colTablero+it_col))       # Se añade esa casilla al conjunto de 'vecinos'

        return vecinos                              # Devuelve el conjunto de vecinos final

    ##### Función encargada de ejecutar el AC3 #####
    def ejecutarAC3(self, tablero):
        
        self.inicializar_matriz(tablero)        # Inicializar la matriz de variables 
        self.inicializar_dominios(tablero)      # y los dominios

        
        aristas = self.generar_restricciones()  # Se obtiene un conjunto de aristas llamando a la función
        
        while aristas:                          # Mientras queden aristas en el conjunto
            arista = aristas.pop()              # Se extrae y elimina la primera de ella
            i, j = arista                       # De una arista se extrae la casilla inicial y la casilla a la que se apunta (i = (x0,y0) y j = (x1,y1))

            if self.reducir_dominios(i, j):     # Si se han hecho cambios en los dominios..
                
                if len(self.matriz_variables[i[0]][i[1]].dominio) == 0:     # Si el dominio se queda vacío, 
                    return False                                            # significa que es inconsistente
                for k in self.obtener_vecinos(i):                           # Se recorre el conjunto de vecinos de la casilla inicial
                    if k != j:                                              # Para no añadir la celda actual
                        aristas.add((k, i))                                 # Agrega nuevas aristas al conjunto 

        return True

###################
# CONSIDERACIONES #
###################
#
#  1. Se vuelve a utilizar un conjunto 'set()' para las aristas y vecinos ya que no debe haber repetidas
#
#  2. En la función 'reducir_dominios' se utiliza una copia del conjunto de dominio 'dominio_i.copy()' 
#     para que al eliminar elementos no cambie su tamaño mientras lo recorremos
#

######################################################################################################################
#####                                             FORWARDCHECKING                                                #####
######################################################################################################################

    def ForwardChecking(self, i, j, tablero):

        for valor in self.matriz_variables[i][j].dominio.copy():    # Se prueban valores del dominio de la casilla
            tablero.setCasilla(i, j, valor)                         # y se coloca 

            if i == FILAS - 1 and j == COLS - 1:                # Es el caso base para verificar que no nos salimos del tablero
                return True
            else:
                next_j = (j + 1) % COLS                         # Calcular la siguiente columna
                next_i = (i + 1) if next_j == 0 else i          # Pasar a la siguiente fila si alcanzamos el final de una fila
                
                if self.forward(i, j, valor):                          # Si al modificar un dominio no se queda vacio
                    if self.ForwardChecking(next_i, next_j, tablero):  # se pasa a la siguiente casilla de forma recursiva
                        return True
                self.restaurar(i, j, tablero)                           # En caso de que el dominio sí que este vacio tras modificarlo, se restaura su valor
                self.numBackJumps += 1                                  # y se suma un salto 
        return False        

    ##### Esta función se encarga de modificar los dominios de las casillas futuras #####
    def forward(self, fila, col, valor):
        
        for k in range(col+1, COLS):                                                # Recorre las columnas que tiene por delante
            if k != col and valor in self.matriz_variables[fila][k].dominio:        # si el valor pasado a la función está en alguna casilla
                self.matriz_variables[fila][k].dominio.remove(valor)                # lo elimina del dominio de la casilla por la que va
                self.matriz_variables[fila][k].podado.add((valor, (fila, col)))     # y lo añade al conjunto de poda junto con su responsable, es decir, la casilla actual

                if not self.matriz_variables[fila][k].dominio:                      # Si al eliminar un valor el dominio se queda vacio
                    return False                                                    # Retorna Falso
                    
        for k in range(fila+1,FILAS):                                               # Recorre las filas que tiene por delante
            if k != fila and valor in self.matriz_variables[k][col].dominio:        # si el valor pasado a la función está en alguna casilla
                self.matriz_variables[k][col].dominio.remove(valor)                 # lo elimina del dominio de la casilla por la que va
                self.matriz_variables[k][col].podado.add((valor, (fila, col)))      # y lo añade al conjunto de poda junto con su responsable, es decir, la casilla actual
                
                if not self.matriz_variables[k][col].dominio:                       # Si al eliminar un valor el dominio se queda vacio
                    return False                                                    # Retorna Falso


        stride = 3                                                                  # Recorre el mini tablero al que pertenece la casilla actual
        filaTablero = (fila // stride) * stride                                     # Misma estructura que la función "estaEnMiniTablero"
        colTablero = (col // stride) * stride
        for it_fila in range(stride):
            for it_col in range(stride):
                if filaTablero + it_fila != fila and colTablero + it_col != col:                                                # Para no añadir la celda actual
                    if valor in self.matriz_variables[filaTablero + it_fila][colTablero + it_col].dominio:                      # Verifica si el valor está en el dominio
                        self.matriz_variables[filaTablero + it_fila][colTablero + it_col].dominio.remove(valor)                 # lo elimina del dominio de la casilla por la que va
                        self.matriz_variables[filaTablero + it_fila][colTablero + it_col].podado.add((valor, (fila, col)))      # y lo añade al conjunto de poda junto con su responsable, es decir, la casilla actual
                        
                        if not self.matriz_variables[filaTablero + it_fila][colTablero + it_col].dominio:               # Si al eliminar un valor el dominio se queda vacio
                            return False                                                                                # Retorna Falso 


        return True

    ##### Esta función se encarga de restaurar valores eliminados de un dominio cuando este se queda vacio #####
    def restaurar(self, i, j, tablero): 

        for fila in range(FILAS) if j < FILAS-1 else range(i+1,FILAS):                  # Recorre el tablero desde la casilla actual en adelante
            for col in range(j, COLS) if fila == i else range(COLS):                    # Para que al primera iteración vaya desde j hasta COLS y las demás desde 0 hasta COLS
                for valor, celda in self.matriz_variables[fila][col].podado.copy():         # Se recorren todos los valores junto con sus responsables del conjunto de podado   
                        if celda == (i,j):                                                  # Si coincide con el buscado
                            self.matriz_variables[fila][col].podado.remove((valor,celda))   # Se elimina del conjunto 'podado'
                            self.matriz_variables[fila][col].dominio.add(valor)             # y se añade de nuevo al dominio correspondiente

    ##### Función encargada de ejecutar el ForwardChecking #####
    def ejecutarForwardChecking(self, tablero):
        self.numBackJumps = 0

        self.inicializar_matriz(tablero)                # Inicializamos la matriz de variables
        self.inicializar_dominios(tablero)              # y los dominios al ejecutar el backtracking

        if self.ForwardChecking(0, 0, tablero):         # Llama a la función de backtracking con la posición inicial (0,0)
            text = "Forward Checking: {} saltos atrás" 
            print(text.format(self.numBackJumps))
            return True
        else:
            return False

###################
# CONSIDERACIONES #
###################
#
#  1. Se vuelve a utilizar un conjunto 'set()' para las podas ya que no admiten repetidas
#
#  2. Se vuelve a utilizar una copia del conjunto de podado 'podado.copy()' 
#     para que al eliminar elementos no cambie su tamaño mientras lo recorremos
import heapq
import time
import psutil
import random

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo_g=0, costo_h=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo_g = costo_g
        self.costo_h = costo_h

    def costo_total(self):
        return self.costo_g + self.costo_h

    def __lt__(self, otro):
        return self.costo_total() < otro.costo_total()

    def obtener_matriz_estado(self):
        return [list(fila) for fila in self.estado]

    def imprimir_estado(self):
        for fila in self.estado:
            print(fila)
        print()

class Operaciones:

    def calcular_costo_h(self, estado, estado_objetivo):
        # Heurística de fichas mal ubicadas
        fichas_mal_ubicadas = 0
        for i in range(3):
            for j in range(3):
                if estado[i][j] != 0 and estado[i][j] != estado_objetivo[i][j]:
                    fichas_mal_ubicadas += 1
        return fichas_mal_ubicadas

    def calcular_costo_g(self, nodo):
        return nodo.costo_g + 1

class Cola():
    def __init__(self):
        self.cola = []

    def cola_vacia(self):
        return len(self.cola) == 0

    def sacar_elemento(self):
        return heapq.heappop(self.cola)

    def agregar_elemento(self, elemento):
        heapq.heappush(self.cola, elemento)

class Resolver:
    def __init__(self, estado_objetivo=None):
        self.estado_inicial = self.generar_estado_inicial()
        self.estado_objetivo = estado_objetivo if estado_objetivo else [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def generar_estado_inicial(self):
        numeros = list(range(9))
        random.shuffle(numeros)
        estado_inicial = [[numeros[i * 3 + j] for j in range(3)] for i in range(3)]
        return estado_inicial

    def obtener_acciones_posibles(self, estado):
        acciones_posibles = []
        fila_vacio = None
        columna_vacio = None
        for i in range(3):
            for j in range(3):
                if estado[i][j] == 0:
                    fila_vacio = i
                    columna_vacio = j
                    break
            if fila_vacio is not None:
                break

        if fila_vacio > 0:
            acciones_posibles.append('abajo')
        if fila_vacio < 2:
            acciones_posibles.append('arriba')
        if columna_vacio > 0:
            acciones_posibles.append('derecha')
        if columna_vacio < 2:
            acciones_posibles.append('izquierda')

        return acciones_posibles

    def es_estado_objetivo(self, estado):
        return estado == self.estado_objetivo

    def funcion_sucesor(self, movimientos, nodo_padre):
        sucesores = []
        calculo = Operaciones()
        for accion in movimientos:
            estado_nuevo = nodo_padre.obtener_matriz_estado()
            fila_vacio = None
            columna_vacio = None

            for i in range(3):
                for j in range(3):
                    if estado_nuevo[i][j] == 0:
                        fila_vacio = i
                        columna_vacio = j
                        break
                if fila_vacio is not None:
                    break

            if accion == 'abajo':
                estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio - 1][columna_vacio] = estado_nuevo[fila_vacio - 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
            elif accion == 'arriba':
                estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio + 1][columna_vacio] = estado_nuevo[fila_vacio + 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
            elif accion == 'derecha':
                estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio - 1] = estado_nuevo[fila_vacio][columna_vacio - 1], estado_nuevo[fila_vacio][columna_vacio]
            elif accion == 'izquierda':
                estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio + 1] = estado_nuevo[fila_vacio][columna_vacio + 1], estado_nuevo[fila_vacio][columna_vacio]

            costo_g_nuevo = calculo.calcular_costo_g(nodo_padre)
            costo_h_nuevo = calculo.calcular_costo_h(estado_nuevo, self.estado_objetivo)
            nodo_nuevo = Nodo(estado_nuevo, nodo_padre, accion, costo_g_nuevo, costo_h_nuevo)
            sucesores.append(nodo_nuevo)
        return sucesores

    def imprimir_pasos(self, nodo):
        pasos = []
        while nodo.accion is not None:
            pasos.append(nodo.accion)
            nodo = nodo.padre
        pasos.reverse()
        estado_actual = self.estado_inicial
        for i, paso in enumerate(pasos, start=1):
            print("Paso {}: mover {}".format(i, paso))
            if paso == 'arriba':
                estado_actual = self.mover_arriba(estado_actual)
            elif paso == 'abajo':
                estado_actual = self.mover_abajo(estado_actual)
            elif paso == 'izquierda':
                estado_actual = self.mover_izquierda(estado_actual)
            elif paso == 'derecha':
                estado_actual = self.mover_derecha(estado_actual)
            for fila in estado_actual:
                print(fila)
            print()

    def mover_arriba(self, estado):
        estado_nuevo = [list(fila) for fila in estado]
        fila_vacio = None
        columna_vacio = None
        for i in range(3):
            for j in range(3):
                if estado_nuevo[i][j] == 0:
                    fila_vacio = i
                    columna_vacio = j
                    break
            if fila_vacio is not None:
                break
        estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio + 1][columna_vacio] = estado_nuevo[fila_vacio + 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
        return estado_nuevo

    def mover_abajo(self, estado):
        estado_nuevo = [list(fila) for fila in estado]
        fila_vacio = None
        columna_vacio = None
        for i in range(3):
            for j in range(3):
                if estado_nuevo[i][j] == 0:
                    fila_vacio = i
                    columna_vacio = j
                    break
            if fila_vacio is not None:
                break
        estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio - 1][columna_vacio] = estado_nuevo[fila_vacio - 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
        return estado_nuevo

    def mover_izquierda(self, estado):
        estado_nuevo = [list(fila) for fila in estado]
        fila_vacio = None
        columna_vacio = None
        for i in range(3):
            for j in range(3):
                if estado_nuevo[i][j] == 0:
                    fila_vacio = i
                    columna_vacio = j
                    break
            if fila_vacio is not None:
                break
        estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio + 1] = estado_nuevo[fila_vacio][columna_vacio + 1], estado_nuevo[fila_vacio][columna_vacio]
        return estado_nuevo

    def mover_derecha(self, estado):
        estado_nuevo = [list(fila) for fila in estado]
        fila_vacio = None
        columna_vacio = None
        for i in range(3):
            for j in range(3):
                if estado_nuevo[i][j] == 0:
                    fila_vacio = i
                    columna_vacio = j
                    break
            if fila_vacio is not None:
                break
        estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio - 1] = estado_nuevo[fila_vacio][columna_vacio - 1], estado_nuevo[fila_vacio][columna_vacio]
        return estado_nuevo

    def Resolver_8_puzzle(self):
        estado_inicial = self.estado_inicial
        estado_objetivo = self.estado_objetivo

        nodo_inicial = Nodo(estado_inicial, None, None, 0, Operaciones().calcular_costo_h(estado_inicial, estado_objetivo))

        frontera = Cola()
        frontera.agregar_elemento(nodo_inicial)

        visitados = set()
        visitados.add(tuple(map(tuple, estado_inicial)))

        while not frontera.cola_vacia():
            nodo_actual = frontera.sacar_elemento()

            if self.es_estado_objetivo(nodo_actual.estado):
                self.imprimir_pasos(nodo_actual)
                return nodo_actual

            movimientos = self.obtener_acciones_posibles(nodo_actual.estado)
            sucesores = self.funcion_sucesor(movimientos, nodo_actual)

            for sucesor in sucesores:
                estado_tuple = tuple(map(tuple, sucesor.estado))
                if estado_tuple not in visitados:
                    frontera.agregar_elemento(sucesor)
                    visitados.add(estado_tuple)

        return None

if __name__ == '__main__':
    resolver = Resolver()
    solucion = resolver.Resolver_8_puzzle()

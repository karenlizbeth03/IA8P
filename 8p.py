import heapq
import random
import time
import tracemalloc

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

class Operaciones:
    def calcular_costo_h(self, estado):
        # Heurística de fichas mal ubicadas
        fichas_mal_ubicadas = sum(1 for i in range(3) for j in range(3) if estado[i][j] != 0 and estado[i][j] != (i * 3 + j))
        return fichas_mal_ubicadas

class Cola:
    def __init__(self):
        self.cola = []

    def cola_vacia(self):
        return len(self.cola) == 0

    def sacar_elemento(self):
        return heapq.heappop(self.cola)

    def agregar_elemento(self, elemento):
        heapq.heappush(self.cola, elemento)

class Resolver:
    def __init__(self):
        self.estado_objetivo = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def generar_estado_inicial(self):
        while True:
            numeros = list(range(9))
            random.shuffle(numeros)
            estado_inicial = [[numeros[i * 3 + j] for j in range(3)] for i in range(3)]
            if self.es_solucionable(estado_inicial):
                return estado_inicial

    def es_solucionable(self, estado):
        estado_1d = [num for fila in estado for num in fila if num != 0]
        inversiones = sum(1 for i in range(len(estado_1d)) for j in range(i + 1, len(estado_1d)) if estado_1d[i] > estado_1d[j])
        return inversiones % 2 == 0

    def encontrar_vacio(self, estado):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == 0:
                    return i, j

    def obtener_acciones_posibles(self, estado):
        acciones_posibles = []
        fila_vacio, columna_vacio = self.encontrar_vacio(estado)

        if fila_vacio > 0: acciones_posibles.append('arriba')
        if fila_vacio < 2: acciones_posibles.append('abajo')
        if columna_vacio > 0: acciones_posibles.append('izquierda')
        if columna_vacio < 2: acciones_posibles.append('derecha')

        return acciones_posibles

    def es_estado_objetivo(self, estado):
        return estado == self.estado_objetivo

    def mover(self, estado, direccion):
        estado_nuevo = [list(fila) for fila in estado]
        fila_vacio, columna_vacio = self.encontrar_vacio(estado_nuevo)

        if direccion == 'abajo' and fila_vacio < 2:
            estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio + 1][columna_vacio] = estado_nuevo[fila_vacio + 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
        elif direccion == 'arriba' and fila_vacio > 0:
            estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio - 1][columna_vacio] = estado_nuevo[fila_vacio - 1][columna_vacio], estado_nuevo[fila_vacio][columna_vacio]
        elif direccion == 'derecha' and columna_vacio < 2:
            estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio + 1] = estado_nuevo[fila_vacio][columna_vacio + 1], estado_nuevo[fila_vacio][columna_vacio]
        elif direccion == 'izquierda' and columna_vacio > 0:
            estado_nuevo[fila_vacio][columna_vacio], estado_nuevo[fila_vacio][columna_vacio - 1] = estado_nuevo[fila_vacio][columna_vacio - 1], estado_nuevo[fila_vacio][columna_vacio]

        return estado_nuevo

    def funcion_sucesor(self, movimientos, nodo_padre):
        sucesores = []
        operaciones = Operaciones()
        for accion in movimientos:
            estado_nuevo = self.mover(nodo_padre.estado, accion)
            costo_g_nuevo = nodo_padre.costo_g + 1
            costo_h_nuevo = operaciones.calcular_costo_h(estado_nuevo)
            nodo_nuevo = Nodo(estado_nuevo, nodo_padre, accion, costo_g_nuevo, costo_h_nuevo)
            sucesores.append(nodo_nuevo)
        return sucesores

    def imprimir_pasos(self, nodo):
        pasos = []
        while nodo:
            pasos.append(nodo)
            nodo = nodo.padre
        pasos.reverse()

        for i, nodo in enumerate(pasos, start=1):
            print(f"Paso {i}: mover {nodo.accion}")
            for fila in nodo.estado:
                print(fila)
            print(f"Costo g: {nodo.costo_g}, Costo h: {nodo.costo_h}, Costo total f: {nodo.costo_total()}\n")

    def Resolver_8_puzzle(self):
        estado_inicial = self.generar_estado_inicial()
        nodo_inicial = Nodo(estado_inicial, None, None, 0, Operaciones().calcular_costo_h(estado_inicial))

        frontera = Cola()
        frontera.agregar_elemento(nodo_inicial)

        visitados = set()
        visitados.add(tuple(map(tuple, estado_inicial)))

        nodos_visitados = 0
        all_nodes = []

        start_time = time.time()
        tracemalloc.start()

        while not frontera.cola_vacia():
            nodo_actual = frontera.sacar_elemento()
            nodos_visitados += 1
            all_nodes.append(nodo_actual)

            if self.es_estado_objetivo(nodo_actual.estado):
                self.imprimir_pasos(nodo_actual)
                break

            movimientos_posibles = self.obtener_acciones_posibles(nodo_actual.estado)
            for sucesor in self.funcion_sucesor(movimientos_posibles, nodo_actual):
                if tuple(map(tuple, sucesor.estado)) not in visitados:
                    visitados.add(tuple(map(tuple, sucesor.estado)))
                    frontera.agregar_elemento(sucesor)

        end_time = time.time()
        tiempo_total = end_time - start_time
        memoria_consumida = tracemalloc.get_traced_memory()[1]
        print(f"\nMedidas de rendimiento:")
        print(f"Nodos visitados (válidos): {nodos_visitados}")
        print(f"Total de nodos generados: {len(all_nodes)}")
        print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
        print(f"Memoria RAM total consumida: {memoria_consumida / 1024:.2f} bytes")

# Ejecutar el resolver
resolver = Resolver()
resolver.Resolver_8_puzzle()

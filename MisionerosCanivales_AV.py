
from collections import deque
from time import perf_counter

# 1. CONFIGURACION DEL PROBLEMA

ESTADO_INICIAL = (3, 3, 1)
ESTADO_OBJETIVO = (0, 0, 0)

# Movimientos posibles del bote:
# (Misioneros, Canibales)
ACCIONES = [
    (2, 0),
    (0, 2),
    (1, 1),
    (1, 0),
    (0, 1)
]

# 2. VALIDACION DE ESTADOS

def estado_valido(estado):

    m, c, bote = estado

    # Verificar limites
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False

    # Personas en la orilla derecha
    mr = 3 - m
    cr = 3 - c

    # Verificar seguridad en ambas orillas
    if m > 0 and c > m:
        return False

    if mr > 0 and cr > mr:
        return False

    return True


# 3. GENERACION DE ESTADOS SUCESORES

def obtener_sucesores(estado):

    m, c, bote = estado
    sucesores = []

    for dm, dc in ACCIONES:

        if bote == 1:
            # El bote cruza de izquierda a derecha

            if dm > m or dc > c:
                continue

            nuevo_estado = (
                m - dm,
                c - dc,
                0
            )

        else:
            # El bote cruza de derecha a izquierda

            mr = 3 - m
            cr = 3 - c

            if dm > mr or dc > cr:
                continue

            nuevo_estado = (
                m + dm,
                c + dc,
                1
            )

        # Verificar que el nuevo estado sea seguro
        if estado_valido(nuevo_estado):

            sucesores.append(
                (nuevo_estado, (dm, dc))
            )

    return sucesores

# 4. ALGORITMO BFS
def busqueda_bfs():

    inicio_tiempo = perf_counter()

    # Cola FIFO
    frontera = deque([
        (ESTADO_INICIAL, [])
    ])

    visitados = {ESTADO_INICIAL}
    nodos_expandidos = 0

    while frontera:

        estado, camino = frontera.popleft()

        # Comprobar si se alcanzo la meta
        if estado == ESTADO_OBJETIVO:

            tiempo = perf_counter() - inicio_tiempo

            return camino, nodos_expandidos, tiempo

        nodos_expandidos += 1

        for siguiente, accion in obtener_sucesores(estado):

            if siguiente not in visitados:

                visitados.add(siguiente)

                nuevo_camino = camino + [accion]

                frontera.append(
                    (siguiente, nuevo_camino)
                )

    return None, nodos_expandidos, perf_counter() - inicio_tiempo


# 5. ALGORITMO DFS
def busqueda_dfs():

    inicio_tiempo = perf_counter()

    # Pila LIFO
    frontera = [
        (ESTADO_INICIAL, [])
    ]

    visitados = {ESTADO_INICIAL}
    nodos_expandidos = 0

    while frontera:

        estado, camino = frontera.pop()

        # Comprobar si se alcanzo la meta
        if estado == ESTADO_OBJETIVO:

            tiempo = perf_counter() - inicio_tiempo

            return camino, nodos_expandidos, tiempo

        nodos_expandidos += 1

        sucesores = obtener_sucesores(estado)

        # Invertir para mantener el orden de acciones
        # al utilizar la pila
        for siguiente, accion in reversed(sucesores):

            if siguiente not in visitados:

                visitados.add(siguiente)

                nuevo_camino = camino + [accion]

                frontera.append(
                    (siguiente, nuevo_camino)
                )

    return None, nodos_expandidos, perf_counter() - inicio_tiempo


# 6. MOSTRAR RESULTADOS
def mostrar_camino(nombre, camino):

    print(f"\n--- SOLUCION {nombre} ---")

    if camino is None:
        print("No se encontro una solucion.")
        return

    estado = ESTADO_INICIAL

    print("Estado inicial:", estado)

    for i, (dm, dc) in enumerate(camino, start=1):

        if estado[2] == 1:
            direccion = "Izquierda -> Derecha"
            nuevo_estado = (
                estado[0] - dm,
                estado[1] - dc,
                0
            )
        else:
            direccion = "Derecha -> Izquierda"
            nuevo_estado = (
                estado[0] + dm,
                estado[1] + dc,
                1
            )

        print(
            f"Paso {i}: {dm} misionero(s), "
            f"{dc} canibal(es) | {direccion}"
        )

        print("Estado:", nuevo_estado)

        estado = nuevo_estado

    print("Estado objetivo:", ESTADO_OBJETIVO)
    print("Longitud del camino:", len(camino))

# 7. BENCHMARKING
def benchmarking(repeticiones=10000):

    print("\n========== BENCHMARKING ==========")

    resultados = {}

    algoritmos = {
        "BFS": busqueda_bfs,
        "DFS": busqueda_dfs
    }

    for nombre, algoritmo in algoritmos.items():

        tiempos = []

        camino = None
        nodos = 0

        for _ in range(repeticiones):

            solucion, expandidos, tiempo = algoritmo()

            camino = solucion
            nodos = expandidos

            tiempos.append(tiempo)

        tiempo_promedio = sum(tiempos) / repeticiones

        resultados[nombre] = {
            "nodos": nodos,
            "tiempo": tiempo_promedio,
            "longitud": len(camino) if camino else 0
        }

    # Mostrar tabla comparativa
    print(
        f"\n{'Algoritmo':<12}"
        f"{'Nodos expandidos':<20}"
        f"{'Tiempo (s)':<18}"
        f"{'Longitud':<12}"
    )

    print("-" * 62)

    for nombre, datos in resultados.items():

        print(
            f"{nombre:<12}"
            f"{datos['nodos']:<20}"
            f"{datos['tiempo']:<18.8f}"
            f"{datos['longitud']:<12}"
        )

    return resultados


# 8. EJECUCION PRINCIPAL

if __name__ == "__main__":

    # Ejecutar BFS
    camino_bfs, nodos_bfs, tiempo_bfs = busqueda_bfs()

    # Ejecutar DFS
    camino_dfs, nodos_dfs, tiempo_dfs = busqueda_dfs()

    # Mostrar las soluciones
    mostrar_camino("BFS", camino_bfs)
    mostrar_camino("DFS", camino_dfs)

    # Comparar rendimiento
    resultados = benchmarking()

    print("\n========== COMPARACION FINAL ==========")

    if resultados["BFS"]["longitud"] <= resultados["DFS"]["longitud"]:
        print("BFS encontro una solucion de longitud menor o igual.")
    else:
        print("DFS encontro una solucion de longitud menor.")

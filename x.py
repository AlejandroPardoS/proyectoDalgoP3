from pyeasyga import pyeasyga
import math

# Calcular distancia euclidiana
def distancia(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

# Construir lista de conexiones válidas
def construir_conexiones(celdas, d):
    conexiones = {}
    n = len(celdas)
    for i in range(n):
        conexiones[i] = []
        id1, x1, y1, pep1 = celdas[i]
        for j in range(i + 1, n):
            id2, x2, y2, pep2 = celdas[j]
            if distancia((x1, y1), (x2, y2)) <= d and set(pep1) & set(pep2):
                conexiones[i].append(j)
                conexiones[j].append(i)
    return conexiones

# Función de fitness
def fitness(individual, conexiones):
    grupos = {}
    for i, grupo in enumerate(individual):
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(i)

    penalizacion = 0
    for grupo, nodos in grupos.items():
        for i in nodos:
            for j in nodos:
                if i != j and j not in conexiones[i]:
                    penalizacion += 1

    return len(set(individual)) - penalizacion

# Crear individuos
def crear_individuo(celdas):
    return [i for i in range(len(celdas))]

# Resolver problema del Ultralisk
def resolver_ultralisk(casos):
    resultados = []
    for n, d, celdas in casos:
        conexiones = construir_conexiones(celdas, d)

        # Configurar GA
        ga = pyeasyga.GeneticAlgorithm(
            celdas,
            population_size=50,
            generations=100,
            crossover_probability=0.8,
            mutation_probability=0.2,
            elitism=True,
            maximise_fitness=False,
        )
        ga.create_individual = crear_individuo
        ga.fitness_function = lambda ind, _: fitness(ind, conexiones)
        
        ga.run()
        solucion = ga.best_individual()[1]

        # Asignar resultados por grupos
        resultados.extend([(i + 1, grupo) for i, grupo in enumerate(solucion)])

    return resultados

# Ejemplo de entrada
casos = [
    (7, 1, [
        (1, 0, 0, ["AETQT", "DFTYA", "PHLYT"]),
        (2, 0, 2, ["DSQTS", "IYHLK", "LHGPS", "LTLLS"]),
        (3, 1, 0, ["AETQT", "DFTYA", "HGCYS", "LSVGG", "SRFNH"]),
        (4, 1, 1, ["DFTYA", "HGCYS", "IYHLK", "SRFNH"]),
        (5, 1, 2, ["DSQTS", "IYHLK", "LSVGG", "LTLLS", "TTVTG"]),
        (6, 2, 1, ["AETQT", "HGCYS", "IYHLK", "LSVGG", "LTLLS"]),
        (7, 2, 2, ["HGCYS", "SRFNH", "TTVTG"]),
    ])
]

# Resolver y mostrar resultados
resultado = resolver_ultralisk(casos)
for r in resultado:
    print(r[0], r[1])

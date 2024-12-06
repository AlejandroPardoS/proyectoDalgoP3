from pyeasyga import pyeasyga
import random
from collections import defaultdict
import sys

def crearArcos(lista_adyacencias, nodoOrigen, nodoFinal):
    if nodoOrigen in lista_adyacencias and nodoFinal not in lista_adyacencias[nodoOrigen]:
            lista_adyacencias[nodoOrigen].append(nodoFinal)

def crearNodo(lista_adyacencias, nodo):
    if nodo not in lista_adyacencias:
        lista_adyacencias[nodo] = []
        
def calcular_distancia_euclidiana(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1/2)

def calcular_distancia_manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
        
def calcularCapacidad(peptidos1, peptidos2):
    return len(set(peptidos1).intersection(set(peptidos2)))

# Calcular la distancia entre dos células
def distancia(celula1, celula2):
    x1, y1 = celula1[1], celula1[2]
    x2, y2 = celula2[1], celula2[2]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Función de fitness
def fitness(individuo, lista_adyacencias):
    grupos = {}
    print(individuo)
    print(lista_adyacencias)
    for celula, grupo in enumerate(individuo, start=1):
        print(celula, grupo)
        grupos[grupo] = []
        grupos[grupo].append(celula)

    penalizacion = 0
    for grupo, miembros in grupos.items():
        for i in miembros:
            for j in miembros:
                if i != j and j not in lista_adyacencias[i]:
                    penalizacion += 1
    return -len(grupos) + penalizacion

# Algoritmo genético usando pyeasyga
def algoritmo_genetico_pyeasyga(num_celulas, lista_adyacencias, generaciones=100, tamano_poblacion=100):
    # Configurar pyeasyga
    ga = pyeasyga.GeneticAlgorithm(
        list(range(num_celulas)),
        population_size=tamano_poblacion,
        generations=generaciones,
        crossover_probability=0.8,
        mutation_probability=0.2,
        elitism=True,
        maximise_fitness=False
    )

    # Definir funciones personalizadas
    def fitness_wrapper(individuo, data):
        return fitness(individuo, lista_adyacencias)

    def create_individual(data):
        return [random.randint(0, num_celulas - 1) for _ in range(num_celulas)]

    def mutate(individuo):
        index = random.randint(0, len(individuo) - 1)
        individuo[index] = random.randint(0, num_celulas - 1)

    # Asignar funciones personalizadas
    ga.fitness_function = fitness_wrapper
    ga.create_individual = create_individual
    ga.mutate_function = mutate

    # Ejecutar algoritmo genético
    ga.run()
    return ga.best_individual()[1]

# Ejecutar el algoritmo para todos los casos de prueba
def main():
    ncasos = int(sys.stdin.readline().strip())
    casos = leer_entrada(ncasos)
    for n, d, celulas in casos:
        lista_adyacencias = generar_lista_adyacencias(celulas, d)
        print(lista_adyacencias)
        mejor_individuo = algoritmo_genetico_pyeasyga(n, lista_adyacencias)

        # Asignar grupos según el mejor individuo
        resultado = [(celulas[i][0], mejor_individuo[i] + 1) for i in range(n)]
        for id_celula, grupo in resultado:
            print(id_celula, grupo)
            
graph = {
    1: [3],
    2: [5],
    3: [1, 4],
    4: [3, 5, 6],
    5: [2, 4, 7],
    6: [4, 7],
    7: [5, 6]
}

mejor_individuo = algoritmo_genetico_pyeasyga(7, graph)
            
def main():
    lista_adyacencias = {}
    ncasos = int(sys.stdin.readline().strip())
    linea = sys.stdin.readline() 
    for i in range(0, ncasos):
        #try :
        numCelulas, dist = linea.split()
        numCelulas, dist = int(numCelulas), int(dist)
        #if numCelulas > 4000:
        #    print("No creemos que nuestro algoritmo resuelva en el tiempo esperado este caso")
        #    continue
        celulas = []
        """crearNodo(lista_adyacencias, "i")
        crearNodo(lista_adyacencias, "f")"""
        for i in range(numCelulas):
            linea = sys.stdin.readline()
            linea = linea.split()
            id = int(linea[0])
            x = int(linea[1])
            y = int(linea[2])
            peptidos = linea[4:]
            celulas.append((id, x, y, peptidos))
            crearNodo(lista_adyacencias, id)
            #print("ID: ", id, "X: ", x, "Y: ", y, "Peptidos: ", peptidos)
            
            for id1, x1, y1, peptidos1 in celulas[:-1]:
                capacidad = calcularCapacidad(peptidos, peptidos1)
                
                if calcular_distancia_euclidiana(x1, y1, x, y) <= dist and capacidad>0:
                    crearArcos(lista_adyacencias, id, id1)
                    crearArcos(lista_adyacencias, id1, id)
            
        #print(lista_adyacencias)
        
        mejor_individuo = algoritmo_genetico_pyeasyga(numCelulas, lista_adyacencias)
        print(mejor_individuo)
        #print(len(minimo))
        #except:
        #    print("Error")
        lista_adyacencias = {}
        linea = sys.stdin.readline()

#main()

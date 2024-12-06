import sys
import random
from pyeasyga import pyeasyga
import math



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



def fitness2(individual, graph):
    nodes_in_clique = [node for node, bit in enumerate(individual, start=1) if bit == 1]
    
    #print(nodes_in_clique)
    for i in nodes_in_clique:
        for j in nodes_in_clique:
            if i != j and (j not in graph[i] and i not in graph[j]):
                #return -len(nodes_in_clique)  # Penalización
                return 0
    return len(nodes_in_clique)

def fitness(individual, lista_adyacencias):
    #print(individual, conexiones)
    grupos = {}
    for nodo, grupo in enumerate(individual, start=1):
        #print(nodo,grupo)
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(nodo)
    #print(grupos.items())
    
    penalizacion = 0
    for grupo, nodos in grupos.items():
        #print(nodos)
        for i in nodos:
            #print(i)
            for j in nodos:
                if i != j and j not in lista_adyacencias[i] and i not in lista_adyacencias[j]:
                    penalizacion += 1

    return len(set(individual)) + penalizacion  # Minimizar grupos y penalizaciones


def create_individual(data):
    return [i for i in range(1, len(data)+1)]

def selection(population):
    #Ruleta
    total_fitness = sum(ind.fitness for ind in population)
    
    if total_fitness == 0:
        return random.choice(population)

    probabilities = []
    cumulative_probability = 0
    for individual in population:
        probability = individual.fitness / total_fitness
        cumulative_probability += probability
        probabilities.append(cumulative_probability)

    r = random.random()
    for i, individual in enumerate(population):
        if r <= probabilities[i]:
            return individual
        
def seleccion_torneo(poblacion, k):
    torneo = random.sample(poblacion, k)
    ganador = min(torneo, key=lambda ind: ind.fitness)
    return ganador



def crossover(parent_1, parent_2):
    point = random.randint(1, len(parent_1) - 1)
    child_1 = parent_1[:point] + parent_2[point:]
    child_2 = parent_2[:point] + parent_1[point:]
    return child_1, child_2


def mutate(individual):
    index = random.randint(0, len(individual) - 1)
    individual[index] = random.randint(1, len(individual) - 1)
    
    
def run_ga_and_collect_data(lista_adyacencias):
    #print(lista_adyacencias)
    ga = pyeasyga.GeneticAlgorithm(
        list(lista_adyacencias.keys()),
        population_size=50,
        generations=100,
        crossover_probability=0.8,
        mutation_probability=0.2,
        elitism=True,
        maximise_fitness=False
    )
    #print("LISTA ADYACENCIAS", lista_adyacencias)
    """
    solucion = {node: random.randint(2,len(lista_adyacencias)) for node in lista_adyacencias}
    #vertice_inicial = random.choice(range(len(data)))
    vertice_inicial = 1
    solucion[vertice_inicial] = 1
    clique_actual = {vertice_inicial}
    #print("ANTES", solucion)
    for node1 in range(2, len(lista_adyacencias)+1):
        if node1 not in clique_actual:
            if all(node1 in lista_adyacencias[node2] and node2 in lista_adyacencias[node1] for node2 in clique_actual):
                solucion[node1] = 1
                clique_actual.add(node1)
                break
              
    print("DESPUES", list(solucion.values()))
    ga.create_individual = lambda _: list(solucion.values())
    """
    ga.create_individual = create_individual
    ga.crossover_function = crossover
    ga.mutate_function = mutate
    ga.fitness_function = lambda ind, _: fitness(ind, lista_adyacencias)
    #ga.selection_function = selection
    ga.selection_function = lambda population: seleccion_torneo(population, int(math.log2(len(population))))
    
    ga.run()
    
    return ga.best_individual()


#grafo = {1: [3], 2: [5], 3: [1, 4], 4: [3, 5, 6], 5: [2, 4, 7], 6: [4, 7], 7: [5, 6]}
#grafo = {1: [3, 4], 2: [4, 5], 3: [1, 4, 5, 6], 4: [1, 2, 3, 5, 6, 7], 5: [2, 3, 4, 6, 7], 6: [3, 4, 5, 7], 7: [4, 5, 6]}
grafo = {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]}

#print(run_ga_and_collect_data(grafo))


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
            peptidos = linea[3:]
            celulas.append((id, x, y, peptidos))
            crearNodo(lista_adyacencias, id)
            #print("ID: ", id, "X: ", x, "Y: ", y, "Peptidos: ", peptidos)
            
            for id1, x1, y1, peptidos1 in celulas[:-1]:
                capacidad = calcularCapacidad(peptidos, peptidos1)
                
                if calcular_distancia_euclidiana(x1, y1, x, y) <= dist and capacidad>0:
                    crearArcos(lista_adyacencias, id, id1)
                    crearArcos(lista_adyacencias, id1, id)
            
        #print(lista_adyacencias)
        numGrupos, mejor_individuo = run_ga_and_collect_data(lista_adyacencias)
        """
        print(mejor_individuo)

        group_mapping = {value: idx for idx, value in enumerate(sorted(set(mejor_individuo)), start=1)}
        
        print(group_mapping)
        for i, group in enumerate(mejor_individuo, start=1):
            print(i, group_mapping[group])
        """
        
        group_mapping = {}
        current_group = 1

        for group in mejor_individuo:
            if group not in group_mapping:
                group_mapping[group] = current_group
                current_group += 1

        # Imprimir los índices y sus nuevos grupos
        for i, group in enumerate(mejor_individuo, start=1):
            print(i, group_mapping[group])
        #except:
        #    print("Error")
        lista_adyacencias = {}
        linea = sys.stdin.readline()
        
main()
import sys
import copy
from itertools import combinations

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

def bron_kerbosch(graph, r, p, x, cliques):
    if not p and not x:
        cliques.append(r)
        return
    for vertex in list(p):
        bron_kerbosch(
            graph,
            r.union([vertex]),
            p.intersection(graph[vertex]),
            x.intersection(graph[vertex]),
            cliques
        )
        p.remove(vertex)
        x.add(vertex)

def find_cliques(graph):
    cliques = []
    bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    return cliques


def min_clique_cover_no_overlap(undirected_graph):
    #undirected_graph = convert_to_undirected(graph)
    cliques = find_cliques(undirected_graph)
    
    # Ordenar las cliques por tamaño descendente
    cliques = sorted(cliques, key=lambda c: -len(c))
    
    uncovered = set(undirected_graph.keys())
    clique_cover = []
    
    while uncovered:
        # Buscar la mayor clique que intersecte con los nodos no cubiertos
        best_clique = max(
            (set(clique) & uncovered for clique in cliques),
            key=lambda c: len(c)
        )
        clique_cover.append(best_clique)
        uncovered -= best_clique  # Eliminar los nodos de la cobertura
    
    return cliques


# Grafo dirigido de ejemplo
graph = {
    1: [3],
    2: [5],
    3: [1, 4],
    4: [3, 5, 6],
    5: [2, 4, 7],
    6: [4, 7],
    7: [5, 6]
}

# Encontrar la mínima cantidad de cliques que cubren todos los vértices
#clique_cover = min_clique_cover_no_overlap(graph)
#print("Cobertura mínima de cliques:", clique_cover)
#print("Cantidad de cliques:", len(clique_cover))

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
        minimo = min_clique_cover_no_overlap(lista_adyacencias)
        print(minimo)
        print(len(minimo))
        #except:
        #    print("Error")
        lista_adyacencias = {}
        linea = sys.stdin.readline()
        
main()

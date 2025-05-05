from concurrent.futures import *
import time
import random

grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

def gerar_grafo_denso(n=100, conexoes_por_no=10, seed=42):
    random.seed(seed)
    grafo = {f'N{i}': [] for i in range(n)}

    for i in range(n):
        vizinhos = random.sample([f'N{j}' for j in range(n) if j != i], conexoes_por_no)
        grafo[f'N{i}'] = vizinhos

    return grafo

# grafo = gerar_grafo_denso()

def bfs(graph, start, end):
    queue = [[start]]
    paths = []
    while queue:
        path = queue.pop()
        node = path[-1]
        if node == end:
            paths.append(path)
        for vertex in graph[node]:
            if vertex not in path:
                queue.append(path + [vertex])
    print(f"Finalizando bfs para Start {start} End {end}")
    return paths

def bfs_parallel(graph, start, end):
    subgraphs = graph.keys()
    print(f"Subgrafos: {subgraphs}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for subgraph in subgraphs:
            print(f"Criando future: Subgrafo {subgraph}")
            futures.append(executor.submit(bfs, graph, subgraph, end))
    
    results = []
    for future in futures:
        results.append(future.result())

    ret = []
    for paths in results:
        for path in paths:
            if path[0] == start and path[-1] == end: # Pegando apenas os caminhos que possuam o inicio e fim desejado
                ret.append(path)
    return ret

if __name__ == "__main__":
    then = time.time()
    print(bfs(grafo, 'A', 'F'))
    now = time.time()
    tempo_serial = now-then
    then = time.time()
    print(bfs_parallel(grafo, 'A', 'F'))
    now = time.time()
    tempo_paralelo = now-then
    print(f"Tempo serial: {tempo_serial:.6f}s")
    print(f"Tempo paralelo: {tempo_paralelo:.6f}s")
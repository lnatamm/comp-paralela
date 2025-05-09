from concurrent.futures import *
import time
import random

# Grafo de exemplo
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Função para gerar um grafo denso para fins de teste
def gerar_grafo_denso(n=100, conexoes_por_no=10, seed=42):
    random.seed(seed)
    #print("Iniciando")
    grafo = {f'N{i}': [] for i in range(n)}

    for i in range(n):
        vizinhos = random.sample([f'N{j}' for j in range(n) if j != i], conexoes_por_no)
        grafo[f'N{i}'] = vizinhos
        print(i)
    #print("Finalizando")

    return grafo

grafo = gerar_grafo_denso(n=10, conexoes_por_no=5)

# Algoritmo BFS
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
    #print(f"Finalizando bfs para Start {start} End {end}")
    return paths

# Função para executar BFS em paralelo
def bfs_parallel(graph, start, end):
    # -- Divisão do grafo em subgrafos (Particionamento)--
    # Cada nó do grafo é considerado um subgrafo
    subgraphs = graph.keys()
    #print(f"Subgrafos: {subgraphs}")

    with ThreadPoolExecutor() as executor:
        # Array para armazenar os resultados
        futures = []
        for subgraph in subgraphs:
            #print(f"Criando future: Subgrafo {subgraph}")
            # Cada subgrafo é processado em paralelo
            # -- Comunicação --
            # Como o grafo é passado como argumento, as taregas não precisam se comunicar entre si
            # -- Aglomeração --
            # Cada tarefa executa o BFS em seu subgrafo
            # -- Mapeamento --
            # Cada bfs é atribuido a um executor, que executa a tarefa em paralelo
            futures.append(executor.submit(bfs, graph, subgraph, end))
    
    results = []
    # Armazenando os resultados
    for future in futures:
        results.append(future.result())

    ret = []
    for paths in results:
        for path in paths:
            if path[0] == start and path[-1] == end: # Pegando apenas os caminhos que possuam o inicio e fim desejado
                ret.append(path)
    return ret

if __name__ == "__main__":
    start = 'N0'
    end = 'N1'
    then = time.time()
    print(bfs(grafo, start, end))
    now = time.time()
    tempo_serial = now-then
    then = time.time()
    print(bfs_parallel(grafo, start, end))
    now = time.time()
    tempo_paralelo = now-then
    print(f"Tempo serial: {tempo_serial:.6f}s")
    print(f"Tempo paralelo: {tempo_paralelo:.6f}s")
from numbers import Number
import sys
import gzip
import numpy as np

def read_graph(input_file):
    graph = {}
    nodes = set()
    sink_nodes = set()

    with gzip.open(input_file, 'rt', encoding='utf-8') as readfile:
        for line in readfile:
            source, target = line.strip().split('\t')
            nodes.update([source, target])

            if source not in graph:
                graph[source] = []
            graph[source].append(target)

        sink_nodes = {page for page in nodes if page not in graph}

    for node in sink_nodes:
        graph[node] = []

    return graph, sink_nodes

def initialize_pagerank(graph):
    num_pages = len(graph)
    initial_pagerank = 1 / num_pages
    pagerank = {page: initial_pagerank for page in graph}
    return pagerank

def update_pagerank(graph, old_pagerank, sink_nodes, lamb):
    sink_node_add = ((1 - lamb) / len(graph)) * sum(old_pagerank[node] for node in sink_nodes)
    new_pagerank = {page: (lamb / len(graph) + sink_node_add) for page in graph}

    for page in graph:
        for neighbor in graph[page]:
            new_pagerank[neighbor] += (1 - lamb) * old_pagerank[page] / len(graph[page])

    return new_pagerank

def compute_inlinks(graph):
    inlinks = {page: 0 for page in graph}
    
    for neighbors in graph.values():
        for neighbor in neighbors:
            inlinks[neighbor] += 1
    return inlinks

def compute_l2_norm(pagerank1, pagerank2):
    return np.linalg.norm(np.array(list(pagerank1.values())) - np.array(list(pagerank2.values())))

def do_pagerank_to_convergence(input_file, lamb, tau,
                               inlinks_file, pagerank_file, k):
    """Iterates the PageRank algorithm until convergence."""
    graph, sinkNodes = read_graph(input_file)
    pagerank = initialize_pagerank(graph)
    prev_pagerank = pagerank.copy()
    
    iteration = 0
    while True:
        pagerank = update_pagerank(graph, pagerank, sinkNodes, lamb)
        iteration += 1
        l2_norm = compute_l2_norm(prev_pagerank, pagerank)
        #print(f"Iteration {iteration}, L2 Norm: {l2_norm}")
        
        if l2_norm < tau:
            break
        
        prev_pagerank = pagerank.copy()
    inLinks = compute_inlinks(graph)

    roundedRanks = {}
    for page in pagerank:
        roundedRanks[page] = round(pagerank[page], 12)
    
    sorted_inlinks = sorted(inLinks.items(), key=lambda x: (-x[1], x[0]), reverse=False)[:k]
    sorted_pagerank = sorted(roundedRanks.items(), key=lambda x: (-x[1], x[0]), reverse=False)[:k]

    with open(pagerank_file, 'w') as file:
        count = 0
        for page, score in sorted_pagerank:
            count += 1
            if count <= 100:
                file.write(f"{page}\t{count}\t{score}\n")
            else:
                break
    with open(inlinks_file, 'w') as file:
        count = 0
        for page, inlinks in sorted_inlinks:
            count += 1
            if count <= 100:
                file.write(f"{page}\t{count}\t{inlinks}\n")
            else:
                break
    
    return


def do_pagerank_n_times(input_file, N, lamb, inlinks_file,
                        pagerank_file, k):
    """Iterates the PageRank algorithm N times."""
    # tested on small.srt.gz
    graph, sinkNodes = read_graph(input_file)
    pagerank = initialize_pagerank(graph)

    for i in range(N):
        pagerank = update_pagerank(graph, pagerank,sinkNodes, lamb)

    inLinks = compute_inlinks(graph)
    roundedRanks = {}
    for page in pagerank:
        roundedRanks[page] = round(pagerank[page], 12)
    
    sorted_inlinks = sorted(inLinks.items(), key=lambda x: (-x[1], x[0]), reverse=False)[:k]
    sorted_pagerank = sorted(roundedRanks.items(), key=lambda x: (-x[1], x[0]), reverse=False)[:k]

    with open(pagerank_file, 'w') as file:
        count = 0
        for page, score in sorted_pagerank:
            count += 1
            if count <= 100:
                file.write(f"{page}\t{count}\t{score}\n")
            else:
                break
    with open(inlinks_file, 'w') as file:
        count = 0
        for page, inlinks in sorted_inlinks:
            count += 1
            if count <= 100:
                file.write(f"{page}\t{count}\t{inlinks}\n")
            else:
                break
    
    return


def main():
    argc = len(sys.argv)
    input_file = sys.argv[1] if argc > 1 else 'links.srt.gz'
    lamb = float(sys.argv[2]) if argc > 2 else 0.2
    
    tau = 0.005
    N = -1  # signals to run until convergence
    if argc > 3:
        arg = sys.argv[3]
        if arg.lower().startswith('exactly'):
            N = int(arg.split(' ')[1])
        else:
            tau = float(arg)
    
    inlinks_file = sys.argv[4] if argc > 4 else 'inlinks.txt'
    pagerank_file = sys.argv[5] if argc > 5 else 'pagerank.txt'
    k = int(sys.argv[6]) if argc > 6 else 100
    
    if N == -1:
        do_pagerank_to_convergence(input_file, lamb, tau, inlinks_file, pagerank_file, k)
    else:
        do_pagerank_n_times(input_file, N, lamb, inlinks_file, pagerank_file, k)
    
    # ...


if __name__ == '__main__':
    main()

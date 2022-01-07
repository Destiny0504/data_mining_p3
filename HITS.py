import os
import re

def create_graph(data_file):
    graph = {} # outgoing graph
    incoming = {} # incoming graph

    nodes = []
    f = open(data_file,'r')
    for data in f.readlines():
        start, dest = tuple(re.findall(r'([\d]+),([\d]+)', data)[0])
        nodes.append(start)
        nodes.append(dest)
        try:
            graph[start] += [dest]
        except:
            graph[start] = [dest]

        try:
            incoming[dest] += [start]
        except:
            incoming[dest] = [start]

    return incoming, graph, list(set(nodes))

def HITS(incoming_graph, outgoing_graph, nodes, itr_times):
    graph_hub = {}
    graph_authority = {}
    for key in nodes:
        graph_authority[key] = 1
        graph_hub[key] = 1
    for _ in range(itr_times):
        total_hub = 0
        total_authority = 0
        for node in nodes:
            graph_authority[node] = 0
            try:
                for incoming in incoming_graph[node]:
                    graph_authority[node] += graph_hub[incoming]
                total_authority += graph_authority[node]
            except:
                pass
        for node in nodes:
            graph_hub[node] = 0
            try:
                for outgoing in outgoing_graph[node]:
                    graph_hub[node] += graph_authority[outgoing]
                total_hub += graph_hub[node]
            except:
                pass
        for node in nodes:
            graph_authority[node] /= total_authority
            graph_hub[node] /= total_hub
    return graph_hub, graph_authority

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_3.txt'
    total_hub = 0
    total_authority = 0
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)

    print(incoming_graph)
    print(outgoing_graph)
    graph_hub, graph_authority = HITS(incoming_graph, outgoing_graph, nodes, 50)

    nodes = sorted(list(nodes))
    for node in nodes:
        print(f'node : {node},  hub : {round(graph_hub[node],3)}, authority : {round(graph_authority[node],3)}')
        total_hub += graph_hub[node]
        total_authority += graph_authority[node]
    print(graph_hub)
    print(graph_authority)

    print(f'total authority : {total_authority} total hub : {total_hub}')
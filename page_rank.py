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

def page_rank(incoming_graph, outgoing_graph, nodes, itr_times, damping_factor):
    page_rank = {}
    base = damping_factor / len(nodes)
    factor = 1 - damping_factor
    total_factor = 0
    for key in nodes:
        try:
            page_rank[key] = 1 / outgoing_graph[key]
        except:
            page_rank[key] = 0

    for _ in range(itr_times):
        for node in nodes:
            page_rank[node] = 0
            page_rank[node] += base
            try:
                for incoming in incoming_graph[node]:
                    page_rank[node] += (page_rank[incoming] / len(outgoing_graph[incoming])) * factor
            except:
                pass
    for key in nodes:
        total_factor += page_rank[key]

    for key in nodes:
        page_rank[key] /= total_factor
    return page_rank

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_3.txt'
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)

    print(incoming_graph)
    print(outgoing_graph)
    page_rank = page_rank(incoming_graph, outgoing_graph, nodes, 50, 0.15)

    nodes = sorted(list(nodes))
    for node in nodes:
        print(f'node : {node},  page_rank : {round(page_rank[node],3)}')
    print(page_rank)

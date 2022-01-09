import os
import re
import numpy as np
def create_graph(data_file):
    graph = {} # outgoing graph
    incoming = {} # incoming graph

    nodes = []
    f = open(data_file,'r')
    # read every line in the file
    for data in f.readlines():
        # using regular expression the get the start node and the end node of an edge
        start, dest = tuple(re.findall(r'([\d]+),([\d]+)', data)[0])
        nodes.append(start)
        nodes.append(dest)
        # Add this edge to the outgoing list of "start node"
        try:
            graph[start] += [dest]
        except:
            graph[start] = [dest]
        # Add this edge to the incoming list of "end node"
        try:
            incoming[dest] += [start]
        except:
            incoming[dest] = [start]

    return incoming, graph, list(set(nodes))

def HITS(incoming_graph, outgoing_graph, nodes, itr_times):
    graph_hub = {}
    graph_authority = {}

    # setting each node's hub and authority to 1
    for key in nodes:
        graph_authority[key] = 1
        graph_hub[key] = 1

    # update each node's authority and hub "itr_times" times
    for _ in range(itr_times):
        total_hub = 0
        total_authority = 0
        # this for-loop updates each node's authority
        for node in nodes:
            graph_authority[node] = 0
            try:
                for incoming in incoming_graph[node]:
                    graph_authority[node] += graph_hub[incoming]
                total_authority += graph_authority[node]
            except:
                pass
        # this for-loop updates each node's hub
        for node in nodes:
            graph_hub[node] = 0
            try:
                for outgoing in outgoing_graph[node]:
                    graph_hub[node] += graph_authority[outgoing]
                total_hub += graph_hub[node]
            except:
                pass
        # normalize each node's hub and authority
        for node in nodes:
            graph_authority[node] /= total_authority
            graph_hub[node] /= total_hub
    return graph_hub, graph_authority

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    # modified graph_?.txt can select which graph you want
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_3.txt'
    total_hub = 0
    total_authority = 0
    authority_list = []
    hub_list = []
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)

    # print(incoming_graph)
    # print(outgoing_graph)
    graph_hub, graph_authority = HITS(incoming_graph, outgoing_graph, nodes, 50)

    nodes = sorted(list(nodes))
    for node in nodes:
        # print(f'node : {node},  hub : {round(graph_hub[node],3)}, authority : {round(graph_authority[node],3)}')
        authority_list.append(round(graph_authority[node],3))
        hub_list.append(round(graph_hub[node],3))
        total_hub += graph_hub[node]
        total_authority += graph_authority[node]
    # print(graph_hub)
    # print(graph_authority)

    authority_list = np.array(authority_list)
    hub_list = np.array(hub_list)

    print(f'authority list : {authority_list}')
    print(f'hub list : {hub_list}')
    # print(f'total authority : {total_authority} total hub : {total_hub}')
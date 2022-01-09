import os
import re
import numpy as np
def create_graph(data_file):
    graph = {} # outgoing graph
    incoming = {} # incoming graph

    nodes = []
    # open the file which you store the data
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

def page_rank(incoming_graph, outgoing_graph, nodes, itr_times, damping_factor):
    page_rank = {}
    # base is the min value of each node
    base = damping_factor / len(nodes)

    # this factor is use for times the incoming node's page rank
    factor = 1 - damping_factor
    total_factor = 0

    # initialize each node's page rank
    for key in nodes:
        try:
            page_rank[key] = 1 / outgoing_graph[key]
        except:
            page_rank[key] = 0

    # update each node's page rank "itr_times" times
    for _ in range(itr_times):
        for node in nodes:
            page_rank[node] = 0
            page_rank[node] += base
            try:
                for incoming in incoming_graph[node]:
                    # counting the page rank
                    page_rank[node] += (page_rank[incoming] / len(outgoing_graph[incoming])) * factor
            except:
                pass

    # count the total page rank
    for key in nodes:
        total_factor += page_rank[key]

    # normalization
    for key in nodes:
        page_rank[key] /= total_factor
    return page_rank

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_6.txt'
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)
    page_rank_list = []

    print(incoming_graph)
    print(outgoing_graph)
    page_rank = page_rank(incoming_graph, outgoing_graph, nodes, 50, 0.15)

    nodes = sorted(list(nodes))
    for node in nodes:
        print(f'node : {node},  page_rank : {round(page_rank[node],3)}')
        page_rank_list.append(round(page_rank[node],3))

    page_rank_list = np.array(page_rank_list)
    print(f'page rank : {page_rank_list}')
    print(page_rank)

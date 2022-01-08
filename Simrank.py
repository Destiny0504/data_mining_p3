import os
import re
import copy

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

def Simrank(incoming_graph, nodes, itr_times, C_factor):
    last_Simrank = {}
    cur_Simrank = {}
    tmp_Simrank = {}
    for key in nodes:
        last_Simrank[key] = {}
        tmp_Simrank[key] ={}
        for node in nodes:
            if key == node:
                last_Simrank[key][node] = 1
                tmp_Simrank[key][node] = 0
            else:
                last_Simrank[key][node] = 0
                tmp_Simrank[key][node] = 0
        try:
            test = incoming_graph[key]
        except:
            incoming_graph[key] = []


    cur_Simrank = copy.deepcopy(tmp_Simrank)

    for _ in range(itr_times):
        for node_a in nodes:
            for node_b in nodes:
                if node_b == node_a:
                    cur_Simrank[node_a][node_b] = 1
                    continue
                try:
                    base = C_factor / (len(incoming_graph[node_b]) * len(incoming_graph[node_a]))
                except:
                    continue
                for incoming_a in incoming_graph[node_a]:
                    for incoming_b in incoming_graph[node_b]:
                        cur_Simrank[node_a][node_b] += last_Simrank[incoming_a][incoming_b]
                cur_Simrank[node_a][node_b] *= base
        last_Simrank = copy.deepcopy(cur_Simrank)
        cur_Simrank = copy.deepcopy(tmp_Simrank)

    return last_Simrank

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_4.txt'
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)

    # print(incoming_graph)

    Sim_rank = Simrank(incoming_graph, nodes, 50, 0.9)

    tmp_sim_1 = []
    sim_rank_list = []

    nodes = sorted(list(nodes))
    for node_a in nodes:
        for node_b in nodes:
            print(f'first node : {node_a}, second node : {node_b},  sim_rank : {round(Sim_rank[node_a][node_b],3)}')
            tmp_sim_1.append(round(Sim_rank[node_a][node_b],3))
        sim_rank_list.append(tmp_sim_1)
        tmp_sim_1 = []

    print(f'Sim_rank :\n{sim_rank_list}')

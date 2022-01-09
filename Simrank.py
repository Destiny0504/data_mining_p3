import os
import re
import copy
from tqdm import tqdm
import time
import numpy as np

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
    # initialize the simrank of each node
    for key in nodes:
        last_Simrank[key] = {}
        tmp_Simrank[key] ={}
        for node in nodes:
            if key == node:
                # if node_a = node_b, then sim rank = 1
                last_Simrank[key][node] = 1
                # tmp_Simrank is a matrix with all 0 value
                tmp_Simrank[key][node] = 0
            else:
                # if node_a != node_b, then sim rank = 0
                last_Simrank[key][node] = 0
                # tmp_Simrank is a matrix with all 0 value
                tmp_Simrank[key][node] = 0
        try:
            test = incoming_graph[key]
        except:
            incoming_graph[key] = []

    # current simrank matrix is a matrix with all 0 in it
    cur_Simrank = copy.deepcopy(tmp_Simrank)

    # update each node's page rank "itr_times" times
    for _ in tqdm(range(itr_times)):
        # every iteration has to update every value in the current matrix
        for node_a in nodes:
            for node_b in nodes:
                if node_b == node_a:
                    cur_Simrank[node_a][node_b] = 1
                    continue
                try:
                    # base is the factor that times simrank
                    base = C_factor / (len(incoming_graph[node_b]) * len(incoming_graph[node_a]))
                except:
                    continue
                # calcuate the sum of simrank of node_a's incoming node and node_b's incoming node
                for incoming_a in incoming_graph[node_a]:
                    for incoming_b in incoming_graph[node_b]:
                        cur_Simrank[node_a][node_b] += last_Simrank[incoming_a][incoming_b]
                cur_Simrank[node_a][node_b] *= base

        # After calculating the Simrank of this iteration,  copy the matrix for the next iteration
        last_Simrank = copy.deepcopy(cur_Simrank)
        cur_Simrank = copy.deepcopy(tmp_Simrank)

    return last_Simrank

if __name__=="__main__":
    cur_file = os.path.abspath(__file__)
    cur_file = re.findall(r'(.*)/[\w]*\.py', cur_file)[0] + '/hw3dataset/graph_6.txt'
    incoming_graph, outgoing_graph, nodes = create_graph(cur_file)

    # print(incoming_graph)
    start = time.time()

    Sim_rank = Simrank(incoming_graph, nodes, 50, 0.9)
    end = time.time()
    tmp_sim_1 = []
    sim_rank_list = []

    nodes = sorted(list(nodes))
    for node_a in nodes:
        for node_b in nodes:
            # print(f'first node : {node_a}, second node : {node_b},  sim_rank : {round(Sim_rank[node_a][node_b],3)}')
            tmp_sim_1.append(round(Sim_rank[node_a][node_b],3))
        sim_rank_list.append(tmp_sim_1)
        tmp_sim_1 = []

    # print(f'Sim_rank :\n{sim_rank_list}')
    # print(f'time : {end - start}')

    sim_rank_list = np.array(sim_rank_list)

    print(f'sim rank :\n{sim_rank_list}')

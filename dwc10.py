# BusBar500kV, 31-Mar-2019
# D-Wave Challenge 10

import networkx as nx
import dwave_networkx as dnx
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler

problem10=[(nx.florentine_families_graph(),'families in Renaissance-era Florence'),
           (nx.karate_club_graph(), 'Karate club'),
           (nx.davis_southern_women_graph(), 'Davis Southern women graph')]
for G,text in problem10:
    shots=1000
    number_of_rounds=10
    min_max_cut_set=[]
    for n in range(number_of_rounds):
        sampler = EmbeddingComposite(DWaveSampler())
        max_cut = dnx.maximum_cut(G, sampler, num_reads=shots)
        min_max_cut_set.append(min(len(max_cut),len(set(G)-set(max_cut))))
    print('Max Cut for %s graph is %s.' % (text,min(min_max_cut_set)))

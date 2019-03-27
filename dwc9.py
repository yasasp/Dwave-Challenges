# BusBar500kV, 26-Mar-2019
# D-Wave Challenge 9

import dwavebinarycsp
from dwave.system.composites import FixedEmbeddingComposite, TilingComposite
from dwave.system.samplers import DWaveSampler

def NEA3SAT(x,y,z):
    if x==y and y==z:
        return False
    else:
        return True

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
csp.add_constraint(NEA3SAT,['a','b','c'])
csp.add_constraint(NEA3SAT,['c','d','e'])

my_bqm = dwavebinarycsp.stitch(csp,min_classical_gap=1)
my_embedding = {'a': {0},
                'b': {7},
                'c': {1, 4},
                'd': {2},
                'e': {6}
                }
# Method 1
print('************ Methord 1 (Embedded in one unit cell) ***************')

sampler1 = FixedEmbeddingComposite(DWaveSampler(), my_embedding)
response = sampler1.sample(my_bqm, num_reads=100)
print('Neighbourhood check : \n',sampler1.adjacency)
print(my_bqm)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)

# Method 2
print('************ Methord 2 (Tiled across a Chimera-structured sampler in multiple unit cell) ***************')

sampler2 = FixedEmbeddingComposite(TilingComposite(DWaveSampler(), 1, 1, 4), my_embedding)
response = sampler2.sample(my_bqm, num_reads=5)
print('Neighbourhood check : \n',sampler2.adjacency)
print(my_bqm)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)



# BusBar500kV, 2-Mar-2019
# D-Wave Challenge 7

import dwavebinarycsp
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler

def NAE3SAT(a,b,c):
    if a==b and b==c:
        return False
    else:
        return True

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
csp.add_constraint(NAE3SAT,['s0','s1','s2'])

my_bqm = dwavebinarycsp.stitch(csp,min_classical_gap=1)

sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(my_bqm, num_reads=5000)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)

my_bqm.to_ising()
print('linear parameters : ',my_bqm.linear)
print('quadratic parameters : ',my_bqm.quadratic)
print('offset parameter : ',my_bqm.offset)

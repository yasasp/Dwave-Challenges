# BusBar500kV, 09-Feb-2019
# D-Wave Challenge 4

import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dimod

shots=100
# Solving as a QUBO Problem
j01=1
h0=-0.2
h1=-0.2
linear = {1: h0, 2: h1}
quadratic = {(1, 2): j01}
bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0.0, dimod.BINARY)

sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads=shots)

print('************ QUBO - Results ************** \n')
for res in response.data(['sample', 'energy', 'num_occurrences']):
    print('|s1 = %s |s2 = %s | Energy = %f | Probability  = %f %% ' % (res.sample[1],res.sample[2],
          res.energy, res.num_occurrences*100/shots))

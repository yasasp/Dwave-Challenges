# BusBar500kV, 18-Feb-2019
# D-Wave Challenge 5

import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dimod

# Test 1: Given QUBO
j01=2
h0=-1
h1=-1
q1=1
q2=5
biases = {(q1,q1): h0, (q2,q2): h1}
coupler_strengths = {(q1,q2): j01}
Q=dict(biases)
Q.update(coupler_strengths)

sampler = dimod.ExactSolver()
response = sampler.sample_qubo(Q)

print('\n************ Test 1 results: Given NOT gate as a QUBO - using Classical Solver to get all states************** \n')
for res in response.data(['sample', 'energy']):
    print('|q1 = %s |q2 = %s | Energy = %f |' % (res.sample[q1],res.sample[q2],
          res.energy))

# Test 2: Finding ising parameters (h,j and offset) - Converting to given qubo to ising using classical solver
j01=2
h0=-1
h1=-1
linear = {1: h0, 2: h1}
quadratic = {(1, 2): j01}
print('\n************ Test 2-A results: Finding Ising parameters (h,j,offset) - converting qubo to ising and reading parameters **************')
bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0, dimod.BINARY)
bqm.to_ising()
bqm_ising = bqm.change_vartype(dimod.SPIN, inplace=False)
linear=bqm_ising.linear
quadratic=bqm_ising.quadratic
offset=bqm_ising.offset
print('Ising linear parameters : ',linear)
print('Ising quadratic parameters : ',quadratic)
print('ising offset parameter : ',offset)
print('\n******* Test 2-B results: Applying Ising parameters found (h,j,offset) - using Classical Solver to get all states********')

sampler = dimod.ExactSolver()
response = sampler.sample(bqm_ising)
for res in response.data(['sample', 'energy']):
    print('|s1 = %s |s2 = %s | Energy = %f |' % (res.sample[1],res.sample[2],
          res.energy))

# Test 3 - Solving as a Ising - ising_sample() method to find the energy off set at ground state
j01=0.5
h0=0
h1=0
linear = {('s0','s0'): h0, ('s1','s1'): h1}
quadratic = {('s0','s1'): j01}

response = dimod.ExactSolver().sample_ising(linear,quadratic)
print('\n************ Test 3 - using sample_ising() method to sjow the energy offset  ************** \n')
for res in response.data(['sample', 'energy']):
    print('|s0 = %s |s1 = %s | Energy = %f |' % (res.sample['s0'],res.sample['s1'],
          res.energy))


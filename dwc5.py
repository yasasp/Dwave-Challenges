# BusBar500kV, 17-Feb-2019
# D-Wave Challenge 5

import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dimod


# Test 1: Solving as a QUBO - Using "manual" embedding (the NOT gate given in the problem)
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

print('\n************ Test 1: QUBO Results - embedding to Classical Solver ************** \n')
for res in response.data(['sample', 'energy']):
    print('|s1 = %s |s2 = %s | Energy = %f |' % (res.sample[q1],res.sample[q2],
          res.energy))

# Test 2: Solving NOT gate as an ising - Converting to BQM from a QUBO and embedded in classical solver
j01=2
h0=-1
h1=-1
linear = {1: h0, 2: h1}
quadratic = {(1, 2): j01}
bqm = dimod.BinaryQuadraticModel(linear, quadratic, 0, dimod.BINARY)
bqm_ising = bqm.change_vartype(dimod.SPIN, inplace=False)

sampler = dimod.ExactSolver()
response = sampler.sample(bqm_ising)
print('\n************ Test 2: Ising Results - converted from QUBO using chage_vartype method **************')
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
print('\n************ Test 3 - using sample_ising() method to find the energy offset for excepted ground state ************** \n')
for res in response.data(['sample', 'energy']):
    if res.sample['s0']==1 and res.sample['s1']==-1:
        energy_off_set=res.energy
        print('energy offset @ excepted ground state is %f' % (energy_off_set))


# Test 4: Solving as a ising using converting to BQM and embedding to with adjusted minum energy gap
j01=0.5
h0=0
h1=0
linear = {1: h0, 2: h1}
quadratic = {(1, 2): j01}
bqm = dimod.BinaryQuadraticModel(linear, quadratic, energy_off_set, dimod.SPIN)

sampler = dimod.ExactSolver()
response = sampler.sample(bqm)
print('\n************ Test 4: Ising Results - converting to BQM and embedding to classical solver **************')
for res in response.data(['sample', 'energy']):
    print('|s1 = %s |s2 = %s | Energy = %f |' % (res.sample[1],res.sample[2],
          res.energy))


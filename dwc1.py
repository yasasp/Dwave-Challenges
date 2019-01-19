# BusBar500kV, 18-Jan-2019
# Trying to Solve the D-Wave Challenge 1

import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import neal

emax=0

def my_ne(s1,s2):
    if s1==s2:
        return False
    else:
        return True

def j_config(j):
    if j==-1 or j==1:
        return True
    else:
        return False

def engy(s1,s2,j):
    global emax
    e=j*s1*s2
    if e>emax:
        emax=e
        return True
    else:
        return False

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)

csp.add_constraint(my_ne,['s1','s2'])
csp.add_constraint(j_config,['j'])
csp.add_constraint(engy,['s1','s2','j'])

for n in range(8, 1, -1):
    try:
        bqm = dwavebinarycsp.stitch(csp, min_classical_gap=2, max_graph_size=n)
    except dwavebinarycsp.exceptions.ImpossibleBQM:
        print('Parameter max_graph_size =', n, ', impossible BQM.')

ans = 'n'
shots = 500
ans = input('Run in Real QC (y/n) :')
if ans == 'y':
    print('Running on Real Quantum Computer...')
    sampler = EmbeddingComposite(DWaveSampler())
    response = sampler.sample(bqm, num_reads=shots)
else:
    print('Running on Annealing Simulator ...')
    sampler = neal.SimulatedAnnealingSampler()
    response = sampler.sample(bqm, num_reads=shots)

print('************ Results ************** \n')
for res in response.data(['sample', 'energy', 'num_occurrences']):
    print('|s1 = %s |s2 = %s |j = %s | Energy = %f | Probability  = %f %% ' % (res.sample['s1'],res.sample['s2'],res.sample['j'],
          res.energy, res.num_occurrences*100/shots))

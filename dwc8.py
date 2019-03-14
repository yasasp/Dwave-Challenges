# BusBar500kV, 14-Mar-2019
# D-Wave Challenge 8

import dwavebinarycsp
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
from dimod import BinaryQuadraticModel, ExactSolver

def NAE3SAT(a,b,c):
    if a==b and b==c:
        return False
    else:
        return True

# Method 1
print('************ Methord 1 (Classical Solver) ***************')
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
csp.add_constraint(NAE3SAT,['a','b','c'])
csp.add_constraint(NAE3SAT,['c','d','e'])

my_bqm = dwavebinarycsp.stitch(csp,min_classical_gap=1)

sampler = ExactSolver()
response = sampler.sample(my_bqm)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)


# Method 2
print('************ Methord 2 (QPU) ***************')
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.SPIN)
ground_states=[(-1,-1, 1),
               (-1, 1, 1),
               ( 1, 1,-1),
               ( 1,-1,-1),
               (-1, 1,-1),
               ( 1,-1, 1)]
constraint1=dwavebinarycsp.Constraint.from_configurations(ground_states,['a','b','c'],'SPIN','nea3sat')
constraint2=dwavebinarycsp.Constraint.from_configurations(ground_states,['c','d','e'],'SPIN','nea3sat')
csp.add_constraint(constraint1)
csp.add_constraint(constraint2)
my_bqm = dwavebinarycsp.stitch(csp)


sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(my_bqm, num_reads=5000)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)


my_bqm.to_ising()
print('linear parameters : ',my_bqm.linear)
print('quadratic parameters : ',my_bqm.quadratic)
print('offset parameter : ',my_bqm.offset)


# Method 3
print('************ Methord 3 (QPU) ***************')
my_bqm = BinaryQuadraticModel(
    linear={}, offset=2, vartype=dwavebinarycsp.SPIN,
    quadratic={
        ('a', 'b'): 1, ('a', 'c'): 1, ('b', 'c'): 1,
        ('c', 'd'): 1, ('c', 'e'): 1, ('d', 'e'): 1
    }
)
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(my_bqm, num_reads=5000)
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    print(list(sample.values()),'Occurrences :',occurrences,'Energey :',energy)

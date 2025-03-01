import numpy as np
import sympy as sym

from dimod import BinaryQuadraticModel, ExactSolver

pr = [2, 3, 3, 4, 7, 5]
dim = len(pr)
s = np.empty(dim, dtype=object)

for i in range (dim):
    s[i] = sym.Symbol(f"s_{i}", bool=True)
    
hamiltonian = sym.expand(np.sum([pr[:]*s[:]])**2)

Q = np.zeros((dim, dim), dtype=float)

for i in range (dim):
    for j in range (i+1, dim):
        Q[i,j] = float(hamiltonian.coeff(s[i]*s[j]))
        
h = {}
for i, qr in enumerate(Q):
    h[(i)] = qr[i]

J={}
for i, qr in enumerate(Q):
    for j, q in enumerate(qr):
        if q != 0:
            J[(i, j)] = q
            
bqm = BinaryQuadraticModel.from_ising(h,J)
sampler = ExactSolver()
sampleset = sampler.sample(bqm)            
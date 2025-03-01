import numpy as np
import sympy as sym
import networkx as nx
from dimod import BinaryQuadraticModel, ExactSolver

node_num = 8

G = nx.Graph()
G.nodes = node_num
G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 5), (1, 3), (1, 4), (1, 6), (1, 7), (2, 3), (3, 5), (4, 7), (7, 3)])

s = np.empty(node_num, dtype=object)
for i in range (node_num):
    s[i] = sym.Symbol(f"s_{i}", bool=True)
    
hamiltonian_A = sym.expand(np.sum(s[:])**2) 

hamiltonian_B = 0
for u, v in G.edges():
    hamiltonian_B = hamiltonian_B + ((1 - s[u]*s[v]) / 2)
    
# hamiltonian_B = sym.expand(np.sum((1-s[u]*s[v])/2) for u, v in G.edges()) 

hamiltonian_T = hamiltonian_A + hamiltonian_B

Q = np.zeros((node_num, node_num), dtype=float)

for i in range (node_num):
    for j in range (i+1, node_num):
        Q[i,j] = float(hamiltonian_T.coeff(s[i]*s[j]))
        
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

print(sampleset)        
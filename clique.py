import numpy as np
import sympy as sym
import networkx as nx
from dimod import BinaryQuadraticModel, ExactSolver

node_num = 7

G = nx.Graph()
G.nodes = node_num
G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 5), (1, 2), (1, 4), (1, 6), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (4, 6), (5, 6)])

s = np.empty(node_num, dtype=object)
for i in range (node_num):
    s[i] = sym.Symbol(f"s_{i}", bool=True)

k = 4
    
hamiltonian_A = sym.expand((k - np.sum(s[:]))**2) 
hamiltonian_A = k*hamiltonian_A

hamiltonian_B = 0
for u, v in G.edges():
    hamiltonian_B = hamiltonian_B + (s[u]*s[v])
hamiltonian_B = k*(k-1)/2 - hamiltonian_B

hamiltonian_T = hamiltonian_A + hamiltonian_B

Q = np.zeros((node_num, node_num), dtype=float)

for i in range (node_num):
    for j in range (i, node_num):
            Q[i,j] = float(hamiltonian_T.coeff(s[i]*s[j]))
            if i == j:
                Q[i, j] = Q[i, j]+float(hamiltonian_T.coeff(s[i]).subs({s[i] : 0 for i in range(node_num)}))
            
bqm = BinaryQuadraticModel.from_qubo(Q)
sampler = ExactSolver()
sampleset = sampler.sample(bqm) 

print(sampleset)        
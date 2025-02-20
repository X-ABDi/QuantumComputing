import numpy as np

def time_evolution(initial_state, hamiltonian, t, hbar=1):
    H = -1j * hamiltonian / hbar
    time_evolution_operator = np.exp(H * t)

    evolved_state = time_evolution_operator @ initial_state

    return evolved_state

def probability_of_desired_state(evolved_state, desired_state):
    inner_product = np.dot(desired_state, evolved_state)
    print(inner_product)
    probability = np.abs(inner_product)**2 

    return probability[0]

# Example usage
if __name__ == "__main__":
    E0 = 5e14*6.62607015e-34
    hamiltonian = np.array([[0, E0, 0], [E0, 0, E0], [0, E0, 0]], dtype=complex)
    initial_state = np.array([[1], [0], [0]], dtype=complex) 
    desired_state = np.array([0, 1, 0], dtype=complex)

    t = 10.0  

    evolved_state = time_evolution(initial_state, hamiltonian, t)
    print(evolved_state)
    prob = probability_of_desired_state(evolved_state, desired_state)

    print(f"Probability at time t={t}: {prob}")

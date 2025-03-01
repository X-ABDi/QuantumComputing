import numpy as np
from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

# Example set
data = np.array([3, 1, 1, 2, 2, 1])

# Function to create the QUBO for the partitioning problem
def create_partition_qubo(data):
    n = len(data)
    total_sum = np.sum(data)

    # Check if the total sum is odd
    if total_sum % 2 != 0:
        raise ValueError("The total sum of the set must be even to partition into two equal subsets.")

    target = total_sum // 2

    # Create the QUBO
    Q = {}
    for i in range(n):
        Q[(i, i)] = data[i]  # Linear terms
        for j in range(i + 1, n):
            Q[(i, j)] = 0  # Initialize quadratic terms

    # Add the constraint that the sum of selected elements should equal target
    for i in range(n):
        for j in range(i + 1, n):
            Q[(i, j)] -= 2 * (target)  # This is the quadratic penalty

    return Q

# Create the QUBO
Q = create_partition_qubo(data)

# Solve the QUBO using a D-Wave sampler
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q, num_reads=100)

# Process the results
print("Solutions:")
for sample in response.samples():
    print(f"Sample: {sample}, Energy: {sample.energy}")

# Extract solution that meets the criteria
for sample in response.samples():
    subset1 = [data[i] for i in range(len(data)) if sample[i] == 1]
    subset2 = [data[i] for i in range(len(data)) if sample[i] == 0]
    if sum(subset1) == sum(subset2):
        print("Valid partition found:")
        print(f"Subset 1: {subset1}, Sum: {sum(subset1)}")
        print(f"Subset 2: {subset2}, Sum: {sum(subset2)}")
        break
else:
    print("No valid partition found.")

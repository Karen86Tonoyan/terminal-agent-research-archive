
import time
import numpy as np
from typing import Dict, List
import sys
import os

# Add the src directory to the path so we can import the module
sys.path.append(os.path.abspath("COLLECTIVE-MIND/src"))
from hybrid_collective_mind import AntColony

def benchmark_get_pheromone_matrix(iterations=10000):
    ac = AntColony(n_ants=20)
    # The default NODES has 4 elements. Let's make it a bit larger for a more meaningful benchmark
    # though I should probably benchmark what's actually there.

    start_time = time.time()
    for _ in range(iterations):
        _ = ac.get_pheromone_matrix()
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total time for {iterations} iterations: {total_time:.4f} seconds")
    print(f"Average time per iteration: {total_time / iterations:.8f} seconds")
    return total_time

if __name__ == "__main__":
    benchmark_get_pheromone_matrix()

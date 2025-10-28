
import random
import math
import time

def cost_function(config: List[int], constraints: Dict[str, Any]) -> float:
    """
    The non-linear, constraint-based cost function (fitness function).
    Goal: Minimize cost (maximize fitness).
    
    In a real system, this would calculate: 
    1. Total allocation latency. 
    2. Constraint violation penalties (e.g., placing two high-load services on one server).
    """
    cost = 0.0
    # Example non-linear cost: penalize configurations that are "too clustered"
    cluster_penalty = sum(abs(config[i] - config[i-1]) for i in range(1, len(config)))
    cost += 10 * (len(config) - cluster_penalty) # High cost for clustering

    # Constraint penalty example: must use resource 5 exactly once
    if config.count(5) != 1:
        cost += 1000  # Major penalty
    
    # Base cost is the sum of resource IDs used
    cost += sum(config)
    return cost

def generate_neighbor(current_config: List[int], total_resources: int) -> List[int]:
    """Generates a neighboring state by randomly swapping two tasks or reassigning one."""
    new_config = list(current_config)
    
    # Randomly pick two indices and swap them (for task assignment change)
    idx1, idx2 = random.sample(range(len(new_config)), 2)
    new_config[idx1], new_config[idx2] = new_config[idx2], new_config[idx1]

    # Optional: Reassign one task to a completely new, valid resource ID
    # new_config[idx1] = random.randint(1, total_resources)
    
    return new_config


def simulated_annealing(initial_config: List[int], constraints: Dict[str, Any], total_resources: int, 
                        T_max: float = 1000, T_min: float = 1, cooling_rate: float = 0.99) -> List[int]:
    """
    The core Simulated Annealing optimization loop.
    T_max: Starting temperature (allows high-cost moves).
    T_min: Stopping temperature.
    cooling_rate: Rate at which temperature drops.
    """
    current_config = initial_config
    current_cost = cost_function(current_config, constraints)
    best_config = current_config
    best_cost = current_cost
    T = T_max
    
    iteration = 0
    start_time = time.time()
    
    while T > T_min and (time.time() - start_time) < 5.0: # Run for max 5 seconds
        neighbor_config = generate_neighbor(current_config, total_resources)
        neighbor_cost = cost_function(neighbor_config, constraints)
        
        delta_cost = neighbor_cost - current_cost
        
        # Acceptance Criteria: always accept better moves (delta_cost < 0)
        # or sometimes accept worse moves (delta_cost >= 0) based on temperature T
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / T):
            current_config = neighbor_config
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_config = current_config
                best_cost = current_cost
        
        T *= cooling_rate
        iteration += 1

    print(f"SA completed in {iteration} iterations.")
    return best_config

# --- Demonstration ---

# Scenario: 10 tasks to be allocated to 6 resources (IDs 1-6)
# Initial random allocation of tasks to resources
initial_tasks = [random.randint(1, 6) for _ in range(10)] 
constraints = {"resource_limit": 6}

print(f"Initial Allocation: {initial_tasks} (Cost: {cost_function(initial_tasks, constraints):.2f})")

optimal_allocation = simulated_annealing(initial_tasks, constraints, total_resources=6)

print(f"\nOptimal Allocation: {optimal_allocation} (Cost: {cost_function(optimal_allocation, constraints):.2f})")

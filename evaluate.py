import time
import gc
from memory_profiler import memory_usage
from dp_unbounded_knapsack import dp_unbounded_knapsack
from bnb_unbounded_knapsack import BnBUnboundedKnapsack

def evaluate(data):
    '''
    Outputs the maximum value that could be obtained from the given knapsack dataset 
    as well as the running time to compute the solution using two algorithms: 
    dynamic programming and branch & bound
    '''
    
    print('Begin evaluation...')
    
    cap = data['cap']
    values = data['values']
    weights = data['weights']
    n = len(values)

    # evaluate dynamic programming algorithm
    print('Evaluating DP algorithm...')

    gc.collect()
    dp_mem_before = max(memory_usage())
    dp_start_time = time.time_ns()
    dp_solution = dp_unbounded_knapsack(cap, n, values, weights)
    dp_end_time = time.time_ns()
    dp_mem_after = max(memory_usage())

    dp_running_time_ns = dp_end_time - dp_start_time
    dp_memory = dp_mem_after - dp_mem_before
        
    print(f"[DP] Solution: ", dp_solution)
    print(f"[DP] Running Time: {dp_running_time_ns} ns")
    print(f"[DP] Memory Used: {dp_memory} MB\n")

    # evaluate branch and bound algorithm
    print('Evaluating BnB algorithm...')
 
    gc.collect()
    bnb_mem_before = max(memory_usage())
    bnb_start_time = time.time_ns()
    bnb_solution, bnb_cert = BnBUnboundedKnapsack(cap, weights, values).solve()
    bnb_end_time = time.time_ns()
    bnb_mem_after = max(memory_usage())

    bnb_running_time_ns = bnb_end_time - bnb_start_time
    bnb_memory = bnb_mem_after - bnb_mem_before
        
    print(f"[BNB] Solution: ", bnb_solution)
    print(f"[BNB] Running Time: {bnb_running_time_ns} ns")
    print(f"[BNB] Memory Used: {bnb_memory} MB\n")

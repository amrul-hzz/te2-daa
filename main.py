from generate_dataset import *
from evaluate import evaluate

# define dataset sizes
SMALL_SIZE, MEDIUM_SIZE, LARGE_SIZE = 100, 1000, 10000

# return dictionaries, each having: knapsack capacity, item value array, item weight array
# generate dataset txt files 
# do not change seed
small_data = generate_dataset(SMALL_SIZE, 42) 
medium_data = generate_dataset(MEDIUM_SIZE, 42) 
large_data = generate_dataset(LARGE_SIZE, 42) 

# demonstration example
# tes = {
#     'cap': 10,
#     'weights': [1, 2, 3],
#     'values': [10, 30, 20],
# }

# export generated data into txt files for viewing
export_to_txt(small_data, 'small_data.txt')
export_to_txt(medium_data, 'medium_data.txt')
export_to_txt(large_data, 'large_data.txt')

# print solution, memory, and running time for each dataset
# NOTE: delete cache, uncomment, and execute only ONE evaluate() in one runtime
print('small dataset\n')
evaluate(small_data)

# print('medium dataset\n')
# evaluate(medium_data)

# print('large dataset\n')
# evaluate(large_data)

# print('contoh penerapan\n')
# evaluate(tes)


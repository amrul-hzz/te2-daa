import random

def export_to_txt(data, filename):
    with open(filename, 'w') as file:
        file.write("Knapsack Capacity: {}\n".format(data['cap']))
        file.write("Item Values: {}\n".format(data['values']))
        file.write("Item Weights: {}\n".format(data['weights']))

def generate_dataset(size, random_seed=None):
    '''
    generates knapsack dataset containing items with possible strong correlation according to the size specified
    '''
    
    if random_seed is not None:
        random.seed(random_seed)

    # generate weight value array 
    weights = [random.randint(1, 100) for _ in range(size)]

    # generate item value array with possible strong correlation to the weights 
    values = [(x + 100) for x in weights]    

    # generate capacity
    cap = int(0.5 * sum(weights))

    data = {
        'cap': cap,
        'weights': weights,
        'values': values,
    }

    return data


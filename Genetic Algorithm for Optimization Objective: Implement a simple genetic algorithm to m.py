import random

# Objective function to maximize: f(x) = x^2
def fitness(x):
    return x ** 2

# Initialize population of binary strings (5 bits -> numbers 0 to 31)
population_size = 6
chromosome_length = 5
generations = 5
mutation_rate = 0.1

population = [bin(random.randint(0, 31))[2:].zfill(chromosome_length) for _ in range(population_size)]

for gen in range(generations):
    # Evaluate fitness
    scored_pop = [(ind, fitness(int(ind, 2))) for ind in population]
    scored_pop.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Generation {gen+1} Best: x = {int(scored_pop[0][0], 2)}, Fitness = {scored_pop[0][1]}")
    
    # Selection (top 50%)
    parents = [ind for ind, fit in scored_pop[:population_size // 2]]
    
    # Crossover & Mutation
    new_population = parents.copy()
    while len(new_population) < population_size:
        p1, p2 = random.choice(parents), random.choice(parents)
        crossover_point = random.randint(1, chromosome_length - 1)
        child = p1[:crossover_point] + p2[crossover_point:]
        
        # Mutation
        child = ''.join([str(1 - int(bit)) if random.random() < mutation_rate else bit for bit in child])
        new_population.append(child)
        
    population = new_population






Sample Input: Population size = 6, Chromosome length = 5 bits, 5 generations.

Sample Output:

Plaintext
Generation 1 Best: x = 31, Fitness = 961
Generation 2 Best: x = 31, Fitness = 961
Generation 3 Best: x = 31, Fitness = 961
Generation 4 Best: x = 31, Fitness = 961
Generation 5 Best: x = 31, Fitness = 961

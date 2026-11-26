import random

# Maximize f(x) = x^2 for x in range [0, 31]
def fitness(x):
    return x ** 2

population = [random.randint(0, 31) for _ in range(6)]

for generation in range(10):
    # Selection: sort by fitness and keep top 3
    population = sorted(population, key=fitness, reverse=True)[:3]
    
    # Crossover & Mutation to refill population
    offspring = []
    while len(offspring) < 3:
        p1, p2 = random.sample(population, 2)
        child = (p1 + p2) // 2
        if random.random() < 0.3:  # Mutation
            child = min(31, max(0, child + random.choice([-1, 1])))
        offspring.append(child)
    population.extend(offspring)

best = max(population, key=fitness)
print(f"Best x: {best}, Maximum f(x) = {fitness(best)}")

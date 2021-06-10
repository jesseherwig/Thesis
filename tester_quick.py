
from model import Population, Citizen, Link

import config


if __name__ == "__main__":
    population = Population()
    population.load_sample()
    output = ''
    population.setInfected(50)
    open('results_quick.txt', 'w')
    with open('results_quick.txt', 'a') as f:
        while config.day < 80:
            population.advanceTime()
            population.print_stats()
            f.write(population.string_stats())
            config.day += 1
        f.close()
    with open('results_final_quick.txt', 'w') as f:
        f.write(population.string_stats())
        f.close()



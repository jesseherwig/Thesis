
from model import Population, Citizen, Link

import config


if __name__ == "__main__":
    population = Population()
    population.load_sample()
    output = ''
    population.setInfected(50)
    open('results_quick2.txt', 'w')
    while config.day < 80:
        population.advanceTime()
        population.print_stats()
        with open('results_quick2.txt', 'a') as f:
            f.write(population.string_stats())
            f.close()
        config.day += 1
    with open('results_final_quick2.txt', 'w') as f:
        f.write(population.string_stats())
        f.close()



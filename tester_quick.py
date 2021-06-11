
from model import Population, Citizen, Link

import config


if __name__ == "__main__":
    population = Population()
    population.load_sample()
    output = ''
    population.setInfected(50)
    while config.day < 80:
        config.day += 1
        population.advanceTime()
        #population.print_stats()
        output += population.string_stats()
        with open('results_quick.txt', 'w') as f:
            f.write(output)
            f.close()
        config.day += 1
    with open('results_final_quick.txt', 'w') as f:
        f.write(population.string_stats())
        f.close()



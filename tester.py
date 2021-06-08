

from model import Population, Citizen, Link

import config


if __name__ == "__main__":
    population = Population()
    population.load_sample()
    output = ''
    while config.day < 3000:
        if config.day == 80:
            population.setInfected(1)
        config.day += 1
        population.advanceTime()
        #population.print_stats()
        output += population.string_stats()
    with open('results.txt', 'w') as f:
        f.write(output)
        f.close()




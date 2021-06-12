import csv

from model import Population

import config


if __name__ == "__main__":
    population = Population()
    population.load_sample()
    output = ''
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Day', 'Total Infections', 'Susceptible', 'Incubating',
                         'Contagious', 'Recovered', 'Deceased', 'Hospitalised', 'Isolated',
                         'AstraZeneca Half Dose', 'AstraZeneca Full Dose',
                         'Pfizer Half Dose', 'Pfizer Full Dose',
                         'Moderna Half Dose', 'Moderna Full Dose', ])
    population.setInfected(50)
    while config.day < 366:
        print(config.day)
        population.advanceTime()
        #population.print_stats()
        output += population.string_stats()
        population.csv_stats('results.csv')
        with open('results.txt', 'w') as f:
            f.write(output)
        config.day += 1
    with open('results_final.txt', 'w') as f:
        f.write(population.string_stats())
        f.close()



import csv

from model import Population

import config


def tester(file_name, runtime):
    population = Population()
    population.load_sample()
    output = ''
    with open(file_name + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Day', 'Total Infections', 'Susceptible', 'Incubating',
                         'Contagious', 'Recovered', 'Deceased', 'Hospitalised', 'Isolated',
                         'AstraZeneca Half Dose', 'AstraZeneca Full Dose',
                         'Pfizer Half Dose', 'Pfizer Full Dose',
                         'Moderna Half Dose', 'Moderna Full Dose', ])
    population.setInfected(50)
    while config.day < runtime:
        config.day += 1
        print(config.day)
        population.advanceTime()
        output += population.string_stats()
        population.csv_stats(file_name + '.csv')
        with open(file_name + '.txt', 'w') as f:
            f.write(output)

    with open(file_name + '_final.txt', 'w') as f:
        f.write(population.string_stats())
        f.close()



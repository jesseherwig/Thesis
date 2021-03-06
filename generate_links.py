import config

import multiprocessing
from random import choices, randrange, random


def generate_links(citizen_num):
    string = ''
    available = list(range(0, config.parameters['size']))
    available.remove(citizen_num)
    destinations = choices(available, k=randrange(0, 100))
    for destination in destinations:
        weight = random()
        string += str(citizen_num) + ',' + str(destination) + ',' + str(weight) + '\n'
        if weight > 0.5:
            string += str(destination) + ',' + str(citizen_num) + ',' + str(weight) + '\n'
    return string


if __name__ == '__main__':
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        string = p.map(generate_links, range(config.parameters['size']))
    with open(config.links_source, 'w') as f:
        f.writelines(string)
        f.close()

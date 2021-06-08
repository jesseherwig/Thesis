from model import Citizen, Link
from random import choices, randrange, random


def generate_citizen():
    sex = choices(['male', 'female'], weights=[493, 507], k=1)
    age = choices([[1, 4], [5, 9], [10, 14], [15, 19], [20, 24], [25, 29], [30, 34],
                   [35, 39], [40, 44], [45, 49], [50, 54], [55, 59], [60, 64], [65, 69],
                   [70, 74], [75, 79], [80, 84], [85, 99]],
                  weights=[63, 64, 60, 61, 67, 71, 73, 67, 68, 68, 65, 62, 56, 51, 38, 28, 20, 21], k=1)
    age = randrange(age[0][0], age[0][1])
    return sex[0] + ',' + str(age) + '\n'


def generate_links(citzen_num, maximum):
    string = ''
    available = list(range(0, maximum))
    available.remove(citzen_num)
    destinations = choices(available, k=randrange(0, 100))
    for destination in destinations:
        weight = random()
        string += str(citzen_num) + ',' + str(destination) + ',' + str(weight) + '\n'
        if weight > 0.5:
            string += str(destination) + ',' + str(citzen_num) + ',' + str(weight) + '\n'
    return string


if __name__ == '__main__':
    number = 1000
    with open('citizens.txt', 'w') as f:
        with open('links.txt', 'w') as g:
            for n in range(number):
                f.write(generate_citizen())
                g.write(generate_links(n, number))
            f.close()
            g.close()

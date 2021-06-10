from random import choices, randrange
import multiprocessing

from config import size as number


def generate_citizen(n):
    sex = choices(['male', 'female'], weights=[493, 507], k=1)
    age = choices([[1, 4], [5, 9], [10, 14], [15, 19], [20, 24], [25, 29], [30, 34],
                   [35, 39], [40, 44], [45, 49], [50, 54], [55, 59], [60, 64], [65, 69],
                   [70, 74], [75, 79], [80, 84], [85, 99]],
                  weights=[63, 64, 60, 61, 67, 71, 73, 67, 68, 68, 65, 62, 56, 51, 38, 28, 20, 21], k=1)
    age = randrange(age[0][0], age[0][1])
    chance = randrange(0, 1000)
    if chance > 990:
        if age >= 50:
            vaccine = choices(('astraZeneca', 'pfizer', 'moderna'), weights=[10, 1, 1], k=1)
        else:
            vaccine = choices(('pfizer', 'moderna'), weights=[51, 50], k=1)
        return sex[0] + ',' + str(age) + ',' + vaccine[0] + '\n'
    else:
        return sex[0] + ',' + str(age) + '\n'


if __name__ == '__main__':
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        string = p.map(generate_citizen, range(4))
    with open('citizens_parallel.txt', 'w') as f:
        f.writelines(string)
        f.close()
